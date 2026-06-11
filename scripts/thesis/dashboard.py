import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import os
import threading
from datetime import datetime

class ThesisDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("EnergyMonitor-OLAP | Thesis Control Center v3.0")
        self.root.geometry("800x600")
        self.root.configure(bg="#0f0f0f")
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # COLOR PALETTE
        BG_DARK = "#121212"
        BG_LIGHT = "#1e1e1e"
        ACCENT_COLOR = "#58a6ff" # Modern soft blue
        TEXT_COLOR = "#e1e4e8"
        FONT_MAIN = ("Segoe UI", 11)
        FONT_HEADER = ("Segoe UI", 18, "bold")
        
        # Налаштування стилів
        self.style.configure("TFrame", background=BG_DARK)
        self.style.configure("TLabel", background=BG_DARK, foreground=TEXT_COLOR, font=FONT_MAIN)
        self.style.configure("Header.TLabel", font=FONT_HEADER, background=BG_DARK, foreground=ACCENT_COLOR)
        self.style.configure("Status.TLabel", font=("Segoe UI", 10), background=BG_DARK, foreground="#8b949e")
        
        self.style.configure("Action.TButton", padding=10, font=("Segoe UI", 11, "bold"), background=BG_LIGHT, foreground=ACCENT_COLOR)
        self.style.map("Action.TButton", 
                       background=[('active', "#1f6feb"), ('disabled', '#21262d')],
                       foreground=[('active', "#ffffff"), ('disabled', '#8b949e')])

        # HEADER
        header_frame = ttk.Frame(root)
        header_frame.pack(pady=20, fill="x")
        header = ttk.Label(header_frame, text="Thesis Generation System v3.0", style="Header.TLabel")
        header.pack(anchor="center")
        
        # MAIN CONTROLS
        ctrl_frame = ttk.Frame(root)
        ctrl_frame.pack(pady=10, padx=20, fill="x")
        
        self.build_btn = ttk.Button(ctrl_frame, text="🚀 Run Full Build", style="Action.TButton", command=self.start_build)
        self.build_btn.pack(side="left", padx=5, expand=True, fill="x")

        self.test_btn = ttk.Button(ctrl_frame, text="🧪 Test Formulas", style="Action.TButton", command=self.test_formulas)
        self.test_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        self.folder_btn = ttk.Button(ctrl_frame, text="📂 Open Folder", style="Action.TButton", command=self.open_folder)
        self.folder_btn.pack(side="left", padx=5, expand=True, fill="x")

        # ROW 2 — Practice Report
        ctrl_frame2 = ttk.Frame(root)
        ctrl_frame2.pack(pady=(0, 10), padx=20, fill="x")
        self.practice_btn = ttk.Button(ctrl_frame2, text="📝 Build Practice Report", style="Action.TButton", command=self.start_practice_build)
        self.practice_btn.pack(side="left", padx=5, expand=True, fill="x")
        self.practice_open_btn = ttk.Button(ctrl_frame2, text="📂 Open Practice Folder", style="Action.TButton", command=self.open_practice_folder)
        self.practice_open_btn.pack(side="left", padx=5, expand=True, fill="x")

        # LOG AREA
        log_frame = ttk.Frame(root)
        log_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        log_header = ttk.Frame(log_frame)
        log_header.pack(fill="x")
        ttk.Label(log_header, text="SYSTEM LOGS:", font=("Consolas", 10, "bold")).pack(side="left")
        
        self.copy_btn = ttk.Button(log_header, text="📋 Copy All Logs", width=15, command=self.copy_logs)
        self.copy_btn.pack(side="right")
        
        self.log_text = scrolledtext.ScrolledText(log_frame, bg="#0d1117", fg="#c9d1d9", 
                                                 insertbackground="#c9d1d9",
                                                 font=("Consolas", 10), state="normal",
                                                 borderwidth=1, relief="solid")
        self.log_text.pack(pady=5, fill="both", expand=True)
        
        # PROGRESS & STATUS
        footer_frame = ttk.Frame(root)
        footer_frame.pack(side="bottom", fill="x", pady=10, padx=20)
        
        self.progress = ttk.Progressbar(footer_frame, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", pady=(0, 5))
        
        self.status_label = ttk.Label(footer_frame, text="Ready. System idle.", style="Status.TLabel")
        self.status_label.pack(side="left")
        
        self.timer_label = ttk.Label(footer_frame, text="", style="Status.TLabel")
        self.timer_label.pack(side="right")

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def copy_logs(self):
        text = self.log_text.get("1.0", "end-1c")
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.log("✔ Logs copied to clipboard.")

    def kill_word(self):
        try:
            subprocess.run(["taskkill", "/F", "/IM", "WINWORD.EXE"], capture_output=True)
            self.log("✅ MS Word killed.")
        except:
            pass

    def open_folder(self):
        path = os.path.abspath("docs/thesis")
        os.startfile(path)
        self.log(f"📂 Folder opened: {path}")

    def open_practice_folder(self):
        path = os.path.abspath("docs/thesis/practice_report")
        os.makedirs(path, exist_ok=True)
        os.startfile(path)
        self.log(f"📂 Practice folder opened: {path}")

    def run_practice_build(self):
        """Merge all PR_*.md sections and convert to DOCX."""
        import time
        start_time = datetime.now()
        try:
            self.practice_btn.config(state="disabled")
            self.progress["value"] = 0
            self.log("=" * 50)
            self.log("📝 BUILDING PRACTICE REPORT...")
            report_dir = os.path.abspath("docs/thesis/practice_report")
            merged_md   = os.path.join(report_dir, "PRACTICE_REPORT_MERGED.md")
            output_docx = os.path.join(report_dir, "PRACTICE_REPORT.docx")
            self.log("Step 1/3: Merging MD sections...")
            section_files = ["PR_TITLE.md","PR_S1.md","PR_S2.md","PR_S3.md","PR_S4.md","PR_S5.md","PR_S6.md"]
            merged_content = []
            for fname in section_files:
                fpath = os.path.join(report_dir, fname)
                if os.path.exists(fpath):
                    with open(fpath, encoding="utf-8") as f:
                        merged_content.append(f.read())
                    self.log(f"  ✔ {fname}")
                else:
                    self.log(f"  ⚠ Missing: {fname}")
            with open(merged_md, "w", encoding="utf-8") as f:
                f.write("\n\n<pagebreak>\n\n".join(merged_content))
            self.progress["value"] = 40
            self.log(f"  Merged → {os.path.basename(merged_md)}")
            self.log("Step 2/3: Converting to DOCX...")
            self.kill_word()
            time.sleep(2)
            conv_proc = subprocess.Popen(
                ["python", "scripts/thesis/convert_thesis.py", merged_md, output_docx],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8"
            )
            for line in conv_proc.stdout:
                line = line.strip()
                if line: self.log(f"  {line}")
            conv_proc.wait()
            self.kill_word()
            time.sleep(1)
            self.progress["value"] = 90
            self.log("Step 3/3: Finalizing...")
            duration = datetime.now() - start_time
            if os.path.exists(output_docx):
                self.progress["value"] = 100
                self.log(f"✅ SUCCESS! Build time: {duration.seconds}s")
                self.log(f"✅ File: {output_docx}")
                if messagebox.askyesno("Practice Report Ready", f"PRACTICE_REPORT.docx is ready!\n\nOpen now?"):
                    os.startfile(os.path.abspath(output_docx))
            else:
                self.log("❌ FAILED: DOCX not found.")
        except Exception as e:
            self.log(f"❌ CRITICAL ERROR: {str(e)}")
        finally:
            self.practice_btn.config(state="normal")

    def start_practice_build(self):
        threading.Thread(target=self.run_practice_build, daemon=True).start()


    def run_build_process(self):
        start_time = datetime.now()
        try:
            self.build_btn.config(state="disabled")
            self.progress["value"] = 0
            self.log("INITIATING THESIS COMPILATION...")
            
            # 1. Kill Word
            self.log("Step 1/4: Cleaning environment...")
            self.kill_word()
            self.progress["value"] = 10
            
            # 2. Batch Conversion
            self.log("Step 2/4: Processing Markdown modules...")
            process = subprocess.Popen(
                ["python", "-u", "scripts/thesis/convert_thesis.py", "--all"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', bufsize=1
            )
            
            for line in process.stdout:
                line = line.strip()
                if line:
                    self.log(f"  {line}")
                    if "Обробка:" in line: self.progress["value"] += 4
            
            process.wait()
            self.progress["value"] = 80
            
            # 3. Merging
            self.log("Step 3/4: Consolidating thesis structure...")
            merge_proc = subprocess.Popen(
                ["python", "scripts/thesis/merge_thesis.py"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8'
            )
            for line in merge_proc.stdout:
                line = line.strip()
                if line: self.log(f"  {line}")
            merge_proc.wait()
            self.progress["value"] = 90
            
            # 4. Final Word Doc
            self.log("Step 4/4: Performing final Word optimization...")
            date_str = datetime.now().strftime("%Y%m%d")
            final_file = f"docs/thesis/Литвиненко_{date_str}.docx"
            
            conv_proc = subprocess.Popen(
                ["python", "scripts/thesis/convert_thesis.py", "docs/thesis/THESIS_FULL_FINAL_UTF8.md", final_file],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8'
            )
            for line in conv_proc.stdout:
                line = line.strip()
                if line: self.log(f"  {line}")
            conv_proc.wait()
            
            duration = datetime.now() - start_time
            if os.path.exists(final_file):
                self.progress["value"] = 100
                self.log(f"✨ SUCCESS! Build time: {duration.seconds}s")
                self.log(f"✨ Final File: {os.path.basename(final_file)}")
                if messagebox.askyesno("Build Success", f"Thesis is ready!\n\nLocation: {final_file}\n\nOpen now?"):
                    os.startfile(os.path.abspath(final_file))
            else:
                self.log("❌ FAILED: Final document not found.")
                
        except Exception as e:
            self.log(f"❌ CRITICAL EXCEPTION: {str(e)}")
        finally:
            self.build_btn.config(state="normal")

    def test_formulas(self):
        def run_test():
            try:
                self.test_btn.config(state="disabled")
                self.log("STARTING FORMULA VALIDATION...")
                self.kill_word()
                
                input_md = "docs/thesis/FORMULA_TEST.md"
                output_docx = "docs/thesis/FORMULA_TEST.docx"
                
                subprocess.run(["python", "scripts/thesis/convert_thesis.py", input_md, output_docx], check=True)
                self.log("✅ Validation successful. Opening test document...")
                os.startfile(os.path.abspath(output_docx))
            except Exception as e:
                self.log(f"❌ Test Error: {e}")
            finally:
                self.test_btn.config(state="normal")
        
        threading.Thread(target=run_test, daemon=True).start()

    def start_build(self):
        threading.Thread(target=self.run_build_process, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    # Dark title bar for Windows (if supported)
    try:
        from ctypes import windll, byref, sizeof, c_int
        HWND = windll.user32.GetParent(root.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(1)), sizeof(c_int))
    except: pass
    
    app = ThesisDashboard(root)
    root.mainloop()
