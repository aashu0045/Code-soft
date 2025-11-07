import sys
import tkinter as tk
from tkinter import messagebox


# ==========================
# GUI IMPLEMENTATION (default)
# ==========================
class CalculatorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Basic Calculator")
        self.root.resizable(False, False)

        self.expression = ""

        self.display_var = tk.StringVar(value="0")
        self.display = tk.Entry(
            root,
            textvariable=self.display_var,
            font=("Segoe UI", 20),
            justify="right",
            bd=8,
            relief=tk.GROOVE,
            state="readonly",
            readonlybackground="white",
        )
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

        self._build_buttons()
        self._configure_grid()

    def _configure_grid(self) -> None:
        for i in range(1, 6):
            self.root.rowconfigure(i, weight=1)
        for j in range(4):
            self.root.columnconfigure(j, weight=1)

    def _build_buttons(self) -> None:
        def btn(text: str, row: int, col: int, cmd) -> None:
            tk.Button(
                self.root, text=text, font=("Segoe UI", 14), command=cmd, width=5, height=2
            ).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        btn("C", 1, 0, self.clear)
        btn("⌫", 1, 1, self.backspace)
        btn("/", 1, 2, lambda: self.add_symbol("/"))
        btn("*", 1, 3, lambda: self.add_symbol("*"))

        btn("7", 2, 0, lambda: self.add_symbol("7"))
        btn("8", 2, 1, lambda: self.add_symbol("8"))
        btn("9", 2, 2, lambda: self.add_symbol("9"))
        btn("-", 2, 3, lambda: self.add_symbol("-"))

        btn("4", 3, 0, lambda: self.add_symbol("4"))
        btn("5", 3, 1, lambda: self.add_symbol("5"))
        btn("6", 3, 2, lambda: self.add_symbol("6"))
        btn("+", 3, 3, lambda: self.add_symbol("+"))

        btn("1", 4, 0, lambda: self.add_symbol("1"))
        btn("2", 4, 1, lambda: self.add_symbol("2"))
        btn("3", 4, 2, lambda: self.add_symbol("3"))
        btn("=", 4, 3, self.evaluate)

        btn("0", 5, 0, lambda: self.add_symbol("0"))
        btn(".", 5, 1, lambda: self.add_symbol("."))
        btn("(", 5, 2, lambda: self.add_symbol("("))
        btn(")", 5, 3, lambda: self.add_symbol(")"))

    def clear(self) -> None:
        self.expression = ""
        self._update_display("0")

    def backspace(self) -> None:
        self.expression = self.expression[:-1]
        self._update_display(self.expression or "0")

    def add_symbol(self, symbol: str) -> None:
        self.expression += symbol
        self._update_display(self.expression)

    def evaluate(self) -> None:
        try:
            result = eval(self.expression, {"__builtins__": {}}, {})
            self.expression = str(result)
            self._update_display(self.expression)
        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot divide by zero.")
        except Exception:
            messagebox.showerror("Error", "Invalid expression.")

    def _update_display(self, text: str) -> None:
        self.display_var.set(text)


def run_gui() -> None:
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


# ==========================
# CLI IMPLEMENTATION (optional via --cli)
# ==========================
def print_header() -> None:
    print("==============================")
    print("     Basic Python Calculator   ")
    print("==============================")


def print_menu() -> None:
    print("Choose an operation:")
    print("  1) Add (+)")
    print("  2) Subtract (-)")
    print("  3) Multiply (*)")
    print("  4) Divide (/)")
    print("  5) Clear screen")
    print("  0) Exit")


def read_number(prompt: str) -> float:
    while True:
        value = input(prompt).strip()
        try:
            return float(value)
        except ValueError:
            print("Invalid number. Please try again, e.g. 12 or 3.5.")


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b


def clear_screen() -> None:
    try:
        import os
        os.system("cls" if sys.platform.startswith("win") else "clear")
    except Exception:
        print("\n" * 50)


def run_cli() -> None:
    clear_screen()
    print_header()

    while True:
        print_menu()
        choice = input("Enter your choice (0-5): ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "5":
            clear_screen()
            print_header()
            continue

        if choice not in {"1", "2", "3", "4"}:
            print("Please choose a valid option: 0, 1, 2, 3, 4, or 5.\n")
            continue

        number_a = read_number("Enter the first number: ")
        number_b = read_number("Enter the second number: ")

        try:
            if choice == "1":
                result = add(number_a, number_b)
                symbol = "+"
            elif choice == "2":
                result = subtract(number_a, number_b)
                symbol = "-"
            elif choice == "3":
                result = multiply(number_a, number_b)
                symbol = "*"
            else:  # choice == "4"
                result = divide(number_a, number_b)
                symbol = "/"

            print(f"\nResult: {number_a} {symbol} {number_b} = {result}\n")
        except ZeroDivisionError as error:
            print(f"Error: {error}\n")

        input("Press Enter to continue...")
        clear_screen()
        print_header()


if __name__ == "__main__":
    if any(arg in ("--cli", "-c") for arg in sys.argv[1:]):
        run_cli()
    else:
        run_gui()

