import tkinter as tk
from tkinter import ttk, messagebox
import string
import secrets
from typing import List


AMBIGUOUS_CHARS = set("Il1O0o`'\"|\\/(){}[]:;,.<>")


def build_alphabets(
	use_lower: bool,
	use_upper: bool,
	use_digits: bool,
	use_symbols: bool,
	avoid_ambiguous: bool,
) -> List[str]:
	alphabets: List[str] = []
	if use_lower:
		letters = string.ascii_lowercase
		if avoid_ambiguous:
			letters = "".join(c for c in letters if c not in AMBIGUOUS_CHARS)
		alphabets.append(letters)
	if use_upper:
		letters = string.ascii_uppercase
		if avoid_ambiguous:
			letters = "".join(c for c in letters if c not in AMBIGUOUS_CHARS)
		alphabets.append(letters)
	if use_digits:
		digits = string.digits
		if avoid_ambiguous:
			digits = "".join(c for c in digits if c not in AMBIGUOUS_CHARS)
		alphabets.append(digits)
	if use_symbols:
		symbols = string.punctuation
		if avoid_ambiguous:
			symbols = "".join(c for c in symbols if c not in AMBIGUOUS_CHARS)
		alphabets.append(symbols)
	return [a for a in alphabets if a]


def generate_password(
	length: int,
	use_lower: bool,
	use_upper: bool,
	use_digits: bool,
	use_symbols: bool,
	avoid_ambiguous: bool,
) -> str:
	if length <= 0:
		raise ValueError("Length must be positive")

	alphabets = build_alphabets(
		use_lower=use_lower,
		use_upper=use_upper,
		use_digits=use_digits,
		use_symbols=use_symbols,
		avoid_ambiguous=avoid_ambiguous,
	)
	if not alphabets:
		raise ValueError("Select at least one character set")

	# Guarantee at least one character from each selected set for better strength
	password_chars: List[str] = []
	for group in alphabets:
		password_chars.append(secrets.choice(group))

	# Fill the rest from the union of all selected characters
	union_chars = "".join(alphabets)
	while len(password_chars) < length:
		password_chars.append(secrets.choice(union_chars))

	# Shuffle using cryptographically secure randomness
	for i in range(len(password_chars) - 1, 0, -1):
		j = secrets.randbelow(i + 1)
		password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

	return "".join(password_chars[:length])


def estimate_strength(length: int, categories_selected: int) -> str:
	# Simple heuristic classifier
	if categories_selected <= 1 or length < 8:
		return "Weak"
	if length < 12:
		return "Medium"
	if categories_selected >= 3 and length >= 12 and length < 16:
		return "Strong"
	if categories_selected >= 3 and length >= 16:
		return "Excellent"
	return "Strong"


class PasswordGeneratorApp:
	def __init__(self, root: tk.Tk) -> None:
		self.root = root
		self.root.title("Password Generator")
		self.root.resizable(False, False)

		self.length_var = tk.IntVar(value=16)
		self.lower_var = tk.BooleanVar(value=True)
		self.upper_var = tk.BooleanVar(value=True)
		self.digits_var = tk.BooleanVar(value=True)
		self.symbols_var = tk.BooleanVar(value=True)
		self.avoid_ambiguous_var = tk.BooleanVar(value=True)
		self.mask_var = tk.BooleanVar(value=False)

		self.password_var = tk.StringVar(value="")
		self.strength_var = tk.StringVar(value="")

		self._build_ui()
		self._update_strength_label()

	def _build_ui(self) -> None:
		frame = ttk.Frame(self.root, padding=12)
		frame.grid(row=0, column=0, sticky="nsew")

		# Length
		length_label = ttk.Label(frame, text="Length:")
		length_label.grid(row=0, column=0, sticky="w")
		length_spin = ttk.Spinbox(
			frame,
			from_=4,
			to=128,
			textvariable=self.length_var,
			width=6,
			command=self._update_strength_label,
		)
		length_spin.grid(row=0, column=1, sticky="w")

		# Options
		options_frame = ttk.LabelFrame(frame, text="Character sets", padding=(10, 6))
		options_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(8, 4))

		lower_cb = ttk.Checkbutton(
			options_frame, text="Lowercase (a-z)", variable=self.lower_var, command=self._update_strength_label
		)
		upper_cb = ttk.Checkbutton(
			options_frame, text="Uppercase (A-Z)", variable=self.upper_var, command=self._update_strength_label
		)
		digits_cb = ttk.Checkbutton(
			options_frame, text="Digits (0-9)", variable=self.digits_var, command=self._update_strength_label
		)
		symbols_cb = ttk.Checkbutton(
			options_frame, text="Symbols (!@#...)", variable=self.symbols_var, command=self._update_strength_label
		)
		ambig_cb = ttk.Checkbutton(
			options_frame, text="Avoid ambiguous characters", variable=self.avoid_ambiguous_var
		)

		lower_cb.grid(row=0, column=0, sticky="w")
		upper_cb.grid(row=0, column=1, sticky="w")
		digits_cb.grid(row=1, column=0, sticky="w")
		symbols_cb.grid(row=1, column=1, sticky="w")
		ambig_cb.grid(row=2, column=0, columnspan=2, sticky="w", pady=(4, 0))

		# Password display
		pw_label = ttk.Label(frame, text="Password:")
		pw_label.grid(row=2, column=0, sticky="w", pady=(8, 0))

		self.password_entry = ttk.Entry(frame, textvariable=self.password_var, width=44)
		self.password_entry.grid(row=2, column=1, columnspan=2, sticky="w", pady=(8, 0))

		mask_cb = ttk.Checkbutton(frame, text="Mask", variable=self.mask_var, command=self._toggle_mask)
		mask_cb.grid(row=2, column=3, sticky="w", padx=(6, 0), pady=(8, 0))

		# Strength
		strength_label = ttk.Label(frame, textvariable=self.strength_var, foreground="#006400")
		strength_label.grid(row=3, column=0, columnspan=4, sticky="w", pady=(6, 0))

		# Actions
		buttons_frame = ttk.Frame(frame)
		buttons_frame.grid(row=4, column=0, columnspan=4, sticky="ew", pady=(10, 0))

		generate_btn = ttk.Button(buttons_frame, text="Generate", command=self._on_generate)
		copy_btn = ttk.Button(buttons_frame, text="Copy", command=self._on_copy)
		generate_btn.grid(row=0, column=0, padx=(0, 8))
		copy_btn.grid(row=0, column=1)

	def _toggle_mask(self) -> None:
		show_char = "*" if self.mask_var.get() else ""
		self.password_entry.config(show=show_char)

	def _on_generate(self) -> None:
		try:
			pwd = generate_password(
				length=int(self.length_var.get()),
				use_lower=bool(self.lower_var.get()),
				use_upper=bool(self.upper_var.get()),
				use_digits=bool(self.digits_var.get()),
				use_symbols=bool(self.symbols_var.get()),
				avoid_ambiguous=bool(self.avoid_ambiguous_var.get()),
			)
			self.password_var.set(pwd)
			self._update_strength_label()
		except ValueError as exc:
			messagebox.showerror("Error", str(exc))

	def _on_copy(self) -> None:
		pwd = self.password_var.get()
		if not pwd:
			messagebox.showinfo("Nothing to copy", "Generate a password first.")
			return
		self.root.clipboard_clear()
		self.root.clipboard_append(pwd)
		self.root.update()  # keep it on clipboard after window closes
		messagebox.showinfo("Copied", "Password copied to clipboard.")

	def _update_strength_label(self) -> None:
		cats = sum(
			bool(v)
			for v in (
				self.lower_var.get(),
				self.upper_var.get(),
				self.digits_var.get(),
				self.symbols_var.get(),
			)
		)
		label = estimate_strength(int(self.length_var.get()), cats)
		self.strength_var.set(f"Strength: {label}")


def main() -> None:
	root = tk.Tk()
	# Use the built-in Tk themed widgets
	try:
		root.style  # type: ignore[attr-defined]
	except Exception:
		pass
	app = PasswordGeneratorApp(root)
	root.mainloop()


if __name__ == "__main__":
	main()


