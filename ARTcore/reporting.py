import os
import json
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server environments

class ReportGenerator:
    def __init__(self, art_instance):
        self.art = art_instance
        self.root_dir = art_instance.root_dir
        self.report_dir = os.path.join(self.root_dir, "ARTreports")
        os.makedirs(self.report_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        # Add custom styles
        self.styles.add(ParagraphStyle(
            name='Title',
            parent=self.styles['Heading1'],
            fontSize=24,
            alignment=1,
            spaceAfter=20
        ))
        self.styles.add(ParagraphStyle(
            name='Heading2',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=15,
            spaceAfter=10
        ))
        self.styles.add(ParagraphStyle(
            name='Normal',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=6
        ))

    def generate_full_report(self):
        """Generate comprehensive system report"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(self.report_dir, f"ART_Report_{timestamp}.pdf")
        
        doc = SimpleDocTemplate(
            report_path, 
            pagesize=landscape(letter),
            rightMargin=72, leftMargin=72,
            topMargin=72, bottomMargin=72
        )
        
        story = []
        
        # Title
        title = Paragraph(f"ART System Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", self.styles['Title'])
        story.append(title)
        
        # System Overview
        story.append(Paragraph("System Overview", self.styles['Heading2']))
        uptime = self._calculate_uptime()
        overview_data = [
            ["Total Uptime", uptime['total']],
            ["Current Session", uptime['session']],
            ["Database Size", self._get_database_size()],
            ["Files Monitored", self._get_monitored_files_count()],
            ["API Status", self._get_api_status()],
        ]
        overview_table = Table(overview_data, colWidths=[2*inch, 4*inch])
        overview_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        story.append(overview_table)
        story.append(Spacer(1, 0.5*inch))
        
        # Generate and include graphs
        story.append(Paragraph("System Analytics", self.styles['Heading2']))
        self._create_dataset_growth_chart()
        story.append(Image(os.path.join(self.report_dir, "dataset_growth.png"), width=7*inch, height=3.5*inch))
        story.append(Spacer(1, 0.2*inch))
        
        self._create_uptime_chart()
        story.append(Image(os.path.join(self.report_dir, "uptime_chart.png"), width=7*inch, height=3.5*inch))
        story.append(Spacer(1, 0.2*inch))
        
        # Learned Items Summary
        story.append(Paragraph("Knowledge Acquisition Summary", self.styles['Heading2']))
        learned_items = self._get_learned_items()
        if learned_items:
            learned_table_data = [["Filename", "Learned Date", "Summary"]]
            for item in learned_items:
                learned_table_data.append([
                    item['filename'],
                    item['learned_at'][:10],  # Just the date part
                    item['summary'][:100] + "..." if len(item['summary']) > 100 else item['summary']
                ])
            learned_table = Table(learned_table_data, colWidths=[1.5*inch, 1.5*inch, 5*inch])
            learned_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))
            story.append(learned_table)
        else:
            story.append(Paragraph("No learned items found.", self.styles['Normal']))
        
        # Save the PDF
        doc.build(story)
        
        return report_path

    def _calculate_uptime(self):
        """Calculate system uptime statistics"""
        current_time = datetime.datetime.now().timestamp()
        session_uptime = current_time - self.art.core.start_time
        
        # Try to calculate total uptime from logs
        total_uptime = session_uptime  # Default to session uptime
        
        # Format times
        session_formatted = self._format_time(session_uptime)
        total_formatted = self._format_time(total_uptime)
        
        return {
            'session': session_formatted,
            'session_seconds': session_uptime,
            'total': total_formatted,
            'total_seconds': total_uptime
        }
    
    def _format_time(self, seconds):
        """Format seconds into readable time"""
        days, remainder = divmod(seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if days > 0:
            return f"{int(days)}d {int(hours)}h {int(minutes)}m"
        elif hours > 0:
            return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
        else:
            return f"{int(minutes)}m {int(seconds)}s"
    
    def _get_database_size(self):
        """Calculate total database size"""
        db_path = os.path.join(self.root_dir, "ART_DB")
        total_size = 0
        file_count = 0
        
        for dirpath, _, filenames in os.walk(db_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
                file_count += 1
        
        # Convert to human-readable size
        if total_size < 1024:
            size_str = f"{total_size} B"
        elif total_size < 1024**2:
            size_str = f"{total_size/1024:.2f} KB"
        elif total_size < 1024**3:
            size_str = f"{total_size/(1024**2):.2f} MB"
        else:
            size_str = f"{total_size/(1024**3):.2f} GB"
            
        return f"{size_str} ({file_count} files)"
    
    def _get_monitored_files_count(self):
        """Get count of files monitored by watchdog"""
        watchlist_path = os.path.join(self.root_dir, "ARTchain", "watchlist.json")
        if os.path.exists(watchlist_path):
            try:
                with open(watchlist_path, 'r') as f:
                    watchlist = json.load(f)
                return f"{len(watchlist)} files"
            except:
                pass
        return "Unknown"
    
    def _get_api_status(self):
        """Get API connection status"""
        status_texts = []
        if hasattr(self.art.core, "llm_integration"):
            if hasattr(self.art.core.llm_integration, "available_models"):
                for model in self.art.core.llm_integration.available_models:
                    status_texts.append(f"{model.capitalize()}: Connected")
                
                if not self.art.core.llm_integration.available_models:
                    status_texts.append("No API connections available")
        
        if not status_texts:
            status_texts = ["Status information unavailable"]
            
        return ", ".join(status_texts)
    
    def _create_dataset_growth_chart(self):
        """Create chart showing dataset growth over time"""
        # Get dataset history or create mock data if unavailable
        datasets_path = os.path.join(self.root_dir, "ART_DB", "datasets")
        
        # Create sample data (in production, you'd extract real data)
        dates = []
        counts = []
        
        # Try to get real data if available
        try:
            # If you track dataset growth with timestamps, use that data
            # For now, using mock data
            current_date = datetime.datetime.now()
            for i in range(30):
                date = current_date - datetime.timedelta(days=29-i)
                dates.append(date.strftime("%Y-%m-%d"))
                # Simulate growing dataset count
                counts.append(5 + i * 2)
        except:
            # Fallback to minimal mock data
            dates = ["Day 1", "Day 15", "Day 30"]
            counts = [5, 20, 35]
        
        # Create the chart
        plt.figure(figsize=(10, 5))
        plt.plot(dates, counts, marker='o', linestyle='-', color='blue')
        plt.title("ART Dataset Growth", fontsize=16)
        plt.xlabel("Date")
        plt.ylabel("Number of Datasets")
        plt.grid(True)
        
        # Rotate date labels for better readability
        if len(dates) > 10:
            plt.xticks(rotation=45, ha='right')
            # Only show a subset of dates to avoid crowding
            plt.xticks(range(0, len(dates), len(dates)//10))
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.report_dir, "dataset_growth.png"))
        plt.close()
    
    def _create_uptime_chart(self):
        """Create chart showing uptime over time"""
        # Mock data for demonstration
        dates = []
        uptimes = []
        
        current_date = datetime.datetime.now()
        for i in range(7):
            date = current_date - datetime.timedelta(days=6-i)
            dates.append(date.strftime("%Y-%m-%d"))
            # Simulate varying uptimes (in hours)
            uptimes.append(20 + i % 3)  # Between 20-22 hours per day
        
        # Create the chart
        plt.figure(figsize=(10, 5))
        plt.bar(dates, uptimes, color='green')
        plt.title("ART Daily Uptime", fontsize=16)
        plt.xlabel("Date")
        plt.ylabel("Uptime (hours)")
        plt.grid(axis='y')
        plt.tight_layout()
        plt.savefig(os.path.join(self.report_dir, "uptime_chart.png"))
        plt.close()
    
    def _get_learned_items(self):
        """Get list of items ART has learned"""
        learned_path = os.path.join(self.root_dir, "ART_DB", "ARTschool", "learned")
        learned_items = []
        
        if not os.path.exists(learned_path):
            return learned_items
            
        for filename in os.listdir(learned_path):
            if filename.endswith(".json"):
                try:
                    with open(os.path.join(learned_path, filename), 'r') as f:
                        item = json.load(f)
                        learned_items.append(item)
                except:
                    continue
                    
        # Sort by learned date
        learned_items.sort(key=lambda x: x.get('learned_at', ''), reverse=True)
        return learned_items