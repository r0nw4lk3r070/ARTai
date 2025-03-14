import tkinter as tk
from tkinter import messagebox
from ARTchain.watchdog_core import Watchdog

def emergency_reset():
    root = tk.Tk()
    root.withdraw()  # Hide window
    watchdog = Watchdog(
        r"C:\Users\r0nw4\ART",
        r"C:\Users\r0nw4\ART\ARTchain\backups",
        r"C:\Users\r0nw4\ART\ARTchain\watchlist.json"
    )
    if messagebox.askyesno("Emergency Reset", "Reset ART to last working state?"):
        watchdog.rollback()
        messagebox.showinfo("Watchdog", "Rollback complete—ART reset!")
    else:
        messagebox.showinfo("Watchdog", "Reset aborted.")
    root.destroy()

if __name__ == "__main__":
    emergency_reset()