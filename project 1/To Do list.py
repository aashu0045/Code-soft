import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog


class ToDoApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("480x520")
        self.root.resizable(False, False)

        self.tasks: list[dict[str, object]] = []
        self.data_file_path = os.path.join(os.path.dirname(__file__), "tasks.json")

        self._build_ui()
        self._bind_shortcuts()
        self._load_tasks_from_disk()

    def _build_ui(self) -> None:
        header_frame = tk.Frame(self.root, padx=10, pady=10)
        header_frame.pack(fill=tk.X)

        title_label = tk.Label(header_frame, text="To-Do List", font=("Segoe UI", 16, "bold"))
        title_label.pack(side=tk.LEFT)

        # Input area
        input_frame = tk.Frame(self.root, padx=10)
        input_frame.pack(fill=tk.X)

        self.task_entry = tk.Entry(input_frame, font=("Segoe UI", 11))
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=(0, 8))

        add_button = tk.Button(input_frame, text="Add", width=10, command=self.add_task)
        add_button.pack(side=tk.LEFT, padx=(8, 0))

        # List area
        list_frame = tk.Frame(self.root, padx=10)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.tasks_var = tk.StringVar(value=[])  # backing variable for Listbox
        self.listbox = tk.Listbox(
            list_frame,
            listvariable=self.tasks_var,
            selectmode=tk.SINGLE,
            font=("Segoe UI", 11),
            activestyle="none",
            height=16,
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        # Action buttons
        actions_frame = tk.Frame(self.root, padx=10, pady=10)
        actions_frame.pack(fill=tk.X)

        edit_button = tk.Button(actions_frame, text="Edit", command=self.edit_selected_task)
        toggle_button = tk.Button(actions_frame, text="Toggle Complete", command=self.toggle_selected_task_completion)
        delete_button = tk.Button(actions_frame, text="Delete", command=self.delete_selected_task)
        clear_completed_button = tk.Button(actions_frame, text="Clear Completed", command=self.clear_completed_tasks)
        save_button = tk.Button(actions_frame, text="Save", command=self.save_tasks_to_disk)
        load_button = tk.Button(actions_frame, text="Load", command=self._load_tasks_from_disk)

        for widget in (edit_button, toggle_button, delete_button, clear_completed_button, save_button, load_button):
            widget.pack(side=tk.LEFT, padx=4)

        # Footer hint
        hint_label = tk.Label(
            self.root,
            text="Tips: Enter=Add, Delete=Remove, Double-click=Toggle, F2=Edit",
            font=("Segoe UI", 9),
            fg="#555",
            padx=10,
            pady=6,
        )
        hint_label.pack(fill=tk.X)

    def _bind_shortcuts(self) -> None:
        self.root.bind("<Return>", lambda _e: self.add_task())
        self.root.bind("<Delete>", lambda _e: self.delete_selected_task())
        self.listbox.bind("<Double-Button-1>", lambda _e: self.toggle_selected_task_completion())
        self.root.bind("<F2>", lambda _e: self.edit_selected_task())

    # ---------- Task operations ----------
    def add_task(self) -> None:
        text = self.task_entry.get().strip()
        if not text:
            messagebox.showinfo("Empty task", "Please type something to add.")
            return
        self.tasks.append({"text": text, "completed": False})
        self.task_entry.delete(0, tk.END)
        self._refresh_listbox()
        self._auto_save()

    def _get_selected_index(self) -> int | None:
        selection = self.listbox.curselection()
        if not selection:
            return None
        return int(selection[0])

    def edit_selected_task(self) -> None:
        index = self._get_selected_index()
        if index is None:
            messagebox.showinfo("No selection", "Select a task to edit.")
            return
        current_text = str(self.tasks[index]["text"])  # type: ignore[index]
        new_text = simpledialog.askstring("Edit Task", "Update the task:", initialvalue=current_text)
        if new_text is None:
            return  # cancelled
        new_text = new_text.strip()
        if not new_text:
            messagebox.showinfo("Empty task", "Task cannot be empty.")
            return
        self.tasks[index]["text"] = new_text
        self._refresh_listbox()
        self._auto_save()

    def toggle_selected_task_completion(self) -> None:
        index = self._get_selected_index()
        if index is None:
            messagebox.showinfo("No selection", "Select a task to toggle.")
            return
        current = bool(self.tasks[index]["completed"])  # type: ignore[index]
        self.tasks[index]["completed"] = not current
        self._refresh_listbox(preserve_selection=index)
        self._auto_save()

    def delete_selected_task(self) -> None:
        index = self._get_selected_index()
        if index is None:
            messagebox.showinfo("No selection", "Select a task to delete.")
            return
        del self.tasks[index]
        self._refresh_listbox()
        self._auto_save()

    def clear_completed_tasks(self) -> None:
        if not self.tasks:
            return
        self.tasks = [t for t in self.tasks if not bool(t.get("completed", False))]
        self._refresh_listbox()
        self._auto_save()

    # ---------- Rendering ----------
    def _format_task_for_display(self, task: dict[str, object]) -> str:
        is_completed = bool(task.get("completed", False))
        prefix = "[✓]" if is_completed else "[ ]"
        return f"{prefix} {task.get('text', '')}"

    def _refresh_listbox(self, preserve_selection: int | None = None) -> None:
        display_values = [self._format_task_for_display(task) for task in self.tasks]
        self.tasks_var.set(display_values)
        if preserve_selection is not None and 0 <= preserve_selection < len(display_values):
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(preserve_selection)
            self.listbox.see(preserve_selection)

    # ---------- Persistence ----------
    def _load_tasks_from_disk(self) -> None:
        if not os.path.exists(self.data_file_path):
            self._refresh_listbox()
            return
        try:
            with open(self.data_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                cleaned: list[dict[str, object]] = []
                for item in data:
                    if isinstance(item, dict) and "text" in item:
                        cleaned.append({
                            "text": str(item.get("text", "")),
                            "completed": bool(item.get("completed", False)),
                        })
                self.tasks = cleaned
        except Exception as exc:  # noqa: BLE001 - show error to user
            messagebox.showerror("Load failed", f"Could not load tasks.json\n\n{exc}")
        finally:
            self._refresh_listbox()

    def save_tasks_to_disk(self) -> None:
        try:
            with open(self.data_file_path, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Saved", "Tasks saved successfully.")
        except Exception as exc:  # noqa: BLE001 - show error to user
            messagebox.showerror("Save failed", f"Could not save tasks.json\n\n{exc}")

    def _auto_save(self) -> None:
        try:
            with open(self.data_file_path, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, indent=2, ensure_ascii=False)
        except Exception:
            # Silent auto-save failure; explicit Save shows errors
            pass


def main() -> None:
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()


