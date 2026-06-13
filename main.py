import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

from database import connection, attendance, income


class AttendanceFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.build_ui()

    def build_ui(self):
        frm = ttk.Frame(self)
        frm.pack(fill=tk.X, padx=8, pady=8)

        ttk.Label(frm, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky=tk.W)
        self.date_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.date_var).grid(row=0, column=1)

        ttk.Label(frm, text="Service Type:").grid(row=1, column=0, sticky=tk.W)
        self.service_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.service_var).grid(row=1, column=1)

        ttk.Label(frm, text="Count:").grid(row=2, column=0, sticky=tk.W)
        self.count_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.count_var).grid(row=2, column=1)

        ttk.Label(frm, text="Note:").grid(row=3, column=0, sticky=tk.W)
        self.note_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.note_var).grid(row=3, column=1)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=8, pady=4)
        ttk.Button(btn_frame, text="Add", command=self.add_record).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Update Selected", command=self.update_selected).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_selected).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh).pack(side=tk.LEFT)

        cols = ("id", "date", "Service Type", "count", "note")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.refresh()

    def add_record(self):
        try:
            cnt = int(self.count_var.get())
        except ValueError:
            messagebox.showerror("Error", "Count must be an integer")
            return
        try:
            rid = attendance.add_attendance(self.date_var.get(), self.service_var.get(), cnt, self.note_var.get())
            messagebox.showinfo("Added", f"Added attendance id {rid}")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        rows = attendance.get_all_attendance()
        for row in rows:
            self.tree.insert("", tk.END, values=(row["id"], row["date"], row["service_type"], row["count"], row["note"]))

    def on_select(self, _ev=None):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        self.date_var.set(vals[1])
        self.service_var.set(vals[2])
        self.count_var.set(vals[3])
        self.note_var.set(vals[4])

    def selected_id(self) -> Optional[int]:
        sel = self.tree.selection()
        if not sel:
            return None
        return int(self.tree.item(sel[0], "values")[0])

    def delete_selected(self):
        rid = self.selected_id()
        if rid is None:
            messagebox.showwarning("Warning", "No record selected")
            return
        attendance.delete_attendance_by_id(rid)
        self.refresh()

    def update_selected(self):
        rid = self.selected_id()
        if rid is None:
            messagebox.showwarning("Warning", "No record selected")
            return
        try:
            cnt = int(self.count_var.get())
        except ValueError:
            messagebox.showerror("Error", "Count must be an integer")
            return
        try:
            attendance.update_attendance(rid, date=self.date_var.get(), service_type=self.service_var.get(), count=cnt, note=self.note_var.get())
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))


class IncomeFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.build_ui()

    def build_ui(self):
        frm = ttk.Frame(self)
        frm.pack(fill=tk.X, padx=8, pady=8)

        ttk.Label(frm, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky=tk.W)
        self.date_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.date_var).grid(row=0, column=1)

        ttk.Label(frm, text="Amount:").grid(row=1, column=0, sticky=tk.W)
        self.amount_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.amount_var).grid(row=1, column=1)

        ttk.Label(frm, text="Category:").grid(row=2, column=0, sticky=tk.W)
        self.category_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.category_var).grid(row=2, column=1)

        ttk.Label(frm, text="Note:").grid(row=3, column=0, sticky=tk.W)
        self.note_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.note_var).grid(row=3, column=1)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=8, pady=4)
        ttk.Button(btn_frame, text="Add", command=self.add_record).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Update Selected", command=self.update_selected).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_selected).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh).pack(side=tk.LEFT)

        cols = ("id", "date", "amount", "category", "note")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.refresh()

    def add_record(self):
        try:
            amt = float(self.amount_var.get())
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            return
        try:
            rid = income.add_income(self.date_var.get(), amt, self.category_var.get(), self.note_var.get())
            messagebox.showinfo("Added", f"Added income id {rid}")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        rows = income.get_all_income()
        for row in rows:
            self.tree.insert("", tk.END, values=(row["id"], row["date"], row["amount"], row["category"], row["note"]))

    def on_select(self, _ev=None):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        self.date_var.set(vals[1])
        self.amount_var.set(vals[2])
        self.category_var.set(vals[3])
        self.note_var.set(vals[4])

    def selected_id(self) -> Optional[int]:
        sel = self.tree.selection()
        if not sel:
            return None
        return int(self.tree.item(sel[0], "values")[0])

    def delete_selected(self):
        rid = self.selected_id()
        if rid is None:
            messagebox.showwarning("Warning", "No record selected")
            return
        income.delete_income_by_id(rid)
        self.refresh()

    def update_selected(self):
        rid = self.selected_id()
        if rid is None:
            messagebox.showwarning("Warning", "No record selected")
            return
        try:
            amt = float(self.amount_var.get())
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            return
        try:
            income.update_income(rid, date=self.date_var.get(), amount=amt, category=self.category_var.get(), note=self.note_var.get())
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ShepherdStats")
        self.geometry("700x500")
        connection.initialize_db()

        nb = ttk.Notebook(self)
        nb.pack(fill=tk.BOTH, expand=True)

        self.att_frame = AttendanceFrame(nb)
        self.inc_frame = IncomeFrame(nb)

        nb.add(self.att_frame, text="Attendance")
        nb.add(self.inc_frame, text="Income")


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
