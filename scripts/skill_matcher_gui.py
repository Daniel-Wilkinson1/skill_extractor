import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

# === GUI Wrapper ===
class SkillMatcherApp:
    def __init__(self, master):
        self.master = master
        master.title("Skill Matcher for HR")
        master.geometry("500x300")

        self.label = tk.Label(master, text="Welcome to the Skill Matcher Tool", font=("Arial", 14))
        self.label.pack(pady=10)

        self.cv_button = tk.Button(master, text="Select CV Folder", command=self.select_cv_folder)
        self.cv_button.pack(pady=5)

        self.jd_button = tk.Button(master, text="Select Job Descriptions Folder", command=self.select_jd_folder)
        self.jd_button.pack(pady=5)

        self.syn_button = tk.Button(master, text="Select Skill Synonyms Excel File", command=self.select_syn_file)
        self.syn_button.pack(pady=5)

        self.run_button = tk.Button(master, text="Run Matching", command=self.run_matching)
        self.run_button.pack(pady=20)

        self.status = tk.Label(master, text="", fg="green")
        self.status.pack()

        self.cv_folder = ""
        self.jd_folder = ""
        self.syn_file = ""

    def select_cv_folder(self):
        self.cv_folder = filedialog.askdirectory()
        self.status.config(text=f"CV folder selected.")

    def select_jd_folder(self):
        self.jd_folder = filedialog.askdirectory()
        self.status.config(text=f"Job description folder selected.")

    def select_syn_file(self):
        self.syn_file = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        self.status.config(text=f"Skill synonyms file selected.")

    def run_matching(self):
        if not all([self.cv_folder, self.jd_folder, self.syn_file]):
            messagebox.showerror("Error", "Please select all required files and folders.")
            return

        # Set environment variables
        env = os.environ.copy()
        env["CV_FOLDER"] = self.cv_folder
        env["JD_FOLDER"] = self.jd_folder
        env["SYNONYM_FILE"] = self.syn_file

        try:
            script_path = os.path.join(os.path.dirname(__file__), "hr_first_filtered_workflow.py")
            subprocess.run(["python", script_path], env=env, check=True)
            messagebox.showinfo("Done", "Matching complete. Files saved in 'data' folder.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Script failed: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SkillMatcherApp(root)
    root.mainloop()
