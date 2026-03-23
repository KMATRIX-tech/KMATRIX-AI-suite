import customtkinter as ctk
from openai import OpenAI
import threading
import os
import pyttsx3
import pyperclip
from PIL import Image
from datetime import datetime
import sys
from tkinter import filedialog

# ==========================================================
# 🔑 KMATRIX CORE ACCESS KEY
# ==========================================================
MY_OPENAI_KEY = "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" 
# ==========================================================

class LicenseAgreement(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("KMATRIX - Security Clearance")
        self.geometry("600x500")
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", sys.exit) 

        self.label = ctk.CTkLabel(self, text="KMATRIX SECURE UPLINK", font=("Orbitron", 20, "bold"), text_color="#00ffff")
        self.label.pack(pady=20)

        self.textbox = ctk.CTkTextbox(self, width=500, height=300, corner_radius=10, fg_color="#0a0a0a", text_color="#00ff00", font=("Consolas", 12))
        self.textbox.pack(pady=10, padx=20)
        
        license_text = f"""
==================================================
KMATRIX PRO AI SUITE - ULTIMATE EDITION
Architect: Keylan Mbilinyi
==================================================

1. This software engine is the exclusive property of 
   Keylan Mbilinyi.
2. Unauthorized cloning, distribution, or reverse 
   engineering is prohibited.
3. KMATRIX provides high-level algorithmic generation. 
   Final code execution is the user's responsibility.

By initializing the core, you accept the KMATRIX 
Tech Global License terms.
        """
        self.textbox.insert("0.0", license_text)
        self.textbox.configure(state="disabled")

        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=20)

        self.btn_accept = ctk.CTkButton(self.btn_frame, text="INITIALIZE CORE", fg_color="#107c10", hover_color="#0b5a0b", font=("Consolas", 12, "bold"), command=self.accept)
        self.btn_accept.grid(row=0, column=0, padx=10)

        self.btn_decline = ctk.CTkButton(self.btn_frame, text="ABORT", fg_color="#a80000", hover_color="#800000", font=("Consolas", 12, "bold"), command=sys.exit)
        self.btn_decline.grid(row=0, column=1, padx=10)

    def accept(self):
        self.destroy()

class KMatrixAI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("KMATRIX Pro - Architect: Keylan Mbilinyi")
        self.geometry("1300x900")
        ctk.set_appearance_mode("dark")
        
        self.withdraw()
        self.after(500, self.show_license)

        try: self.after(200, lambda: self.iconbitmap("kmatrix_icon.ico"))
        except: pass

        self.client = OpenAI(api_key=MY_OPENAI_KEY)
        self.current_mode = "Expert Coder"
        self.last_ai_response = ""
        self.chat_history = []

        # --- Layout ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=320, fg_color="#030303", border_width=1, border_color="#111111")
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        try:
            self.logo_img = ctk.CTkImage(Image.open("kmatrix_logo.png"), size=(140, 140))
            ctk.CTkLabel(self.sidebar, image=self.logo_img, text="").pack(pady=(40, 10))
        except: 
            ctk.CTkLabel(self.sidebar, text="[ K ]", font=("Orbitron", 60, "bold"), text_color="#00ffff").pack(pady=(40, 10))

        ctk.CTkLabel(self.sidebar, text="KMATRIX", font=("Fixedsys", 38, "bold"), text_color="#00ffff").pack()
        ctk.CTkLabel(self.sidebar, text="By Keylan Mbilinyi", font=("Segoe UI", 12, "italic"), text_color="#666666").pack(pady=(0, 20))

        self.btn_new = ctk.CTkButton(self.sidebar, text="⚡ REBOOT SYSTEM", fg_color="#0078d4", corner_radius=6, command=self.new_chat)
        self.btn_new.pack(pady=10, padx=25, fill="x")

        self.btn_copy = ctk.CTkButton(self.sidebar, text="📋 CLONE LAST CODE", fg_color="#1a1a1a", border_width=1, border_color="#333", corner_radius=6, command=self.copy_to_clipboard)
        self.btn_copy.pack(pady=5, padx=25, fill="x")
        
        self.btn_export = ctk.CTkButton(self.sidebar, text="💾 EXPORT LOG", fg_color="#1a1a1a", border_width=1, border_color="#333", corner_radius=6, command=self.export_chat)
        self.btn_export.pack(pady=5, padx=25, fill="x")

        self.voice_switch = ctk.CTkSwitch(self.sidebar, text="🔊 Vocal Interface", progress_color="#00ffff")
        self.voice_switch.select()
        self.voice_switch.pack(pady=20, padx=25)

        self.mode_menu = ctk.CTkOptionMenu(self.sidebar, values=["Expert Coder", "Cyber Security", "Full-Stack Dev", "Data Scientist", "God Mode"], fg_color="#0a0a0a", button_color="#0078d4", command=self.change_mode)
        self.mode_menu.set("Expert Coder")
        self.mode_menu.pack(pady=10, padx=25, fill="x")

        # System Status Card
        self.status_frame = ctk.CTkFrame(self.sidebar, fg_color="#0a0a0a", corner_radius=8, border_width=1, border_color="#111")
        self.status_frame.pack(pady=20, padx=20, fill="both", expand=True)
        ctk.CTkLabel(self.status_frame, text="SYSTEM STATUS", font=("Consolas", 11, "bold"), text_color="#00ffff").pack(pady=10)
        status_text = f"Host: KMATRIX-PRIME\nUplink: Active\nEngine: GPT-4o\nDev: Mbilinyi"
        ctk.CTkLabel(self.status_frame, text=status_text, font=("Consolas", 10), text_color="#00ff00", justify="left").pack(pady=5, padx=10, anchor="w")

        # 2. MAIN TERMINAL
        self.chat_display = ctk.CTkTextbox(self, corner_radius=15, font=("Consolas", 15), fg_color="#080808", border_width=1, border_color="#1a1a1a", text_color="#e0e0e0", wrap="word")
        self.chat_display.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="nsew")
        self.chat_display.configure(state="disabled")

        # 3. INPUT
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.progress_bar = ctk.CTkProgressBar(self.input_frame, mode="indeterminate", height=4, progress_color="#00ffff")
        self.progress_bar.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0)

        self.user_input = ctk.CTkTextbox(self.input_frame, height=80, corner_radius=10, font=("Consolas", 14), fg_color="#111", border_width=1, border_color="#333", text_color="#fff")
        self.user_input.grid(row=1, column=0, padx=(0, 15), sticky="ew")
        self.user_input.bind("<Return>", self.handle_enter)

        self.send_btn = ctk.CTkButton(self.input_frame, text="EXECUTE", width=140, height=80, corner_radius=10, fg_color="#0078d4", font=("Orbitron", 14, "bold"), command=self.start_chat_thread)
        self.send_btn.grid(row=1, column=1)

        self.reset_memory()

    # --- LOGIC ---
    def show_license(self):
        LicenseAgreement(self)
        self.deiconify()

    def handle_enter(self, event):
        if event.state & 0x0001: 
            return None 
        else:
            self.start_chat_thread()
            return "break"

    def speak(self, text):
        if self.voice_switch.get() == 1:
            try:
                engine = pyttsx3.init()
                engine.setProperty('rate', 180)
                clean_text = text.replace("```", "").replace("#", "").replace("*", "")
                engine.say(clean_text)
                engine.runAndWait()
            except: pass

    def reset_memory(self):
        sys_prompts = {
            "Expert Coder": "You are KMATRIX by Keylan Mbilinyi. Mastery: All code. Be professional and concise.",
            "Cyber Security": "You are a Cyber Security AI. Focus on protection and analysis.",
            "Full-Stack Dev": "You are a Master Full-Stack Developer.",
            "Data Scientist": "You are a Data Science logic engine.",
            "God Mode": "Absolute intelligence mode activated. Provide ultimate clarity."
        }
        self.chat_history = [{"role": "system", "content": sys_prompts.get(self.current_mode)}]

    def change_mode(self, choice):
        self.current_mode = choice
        self.new_chat()

    def copy_to_clipboard(self):
        if self.last_ai_response:
            pyperclip.copy(self.last_ai_response)
            self.btn_copy.configure(text="✅ CLONED", fg_color="#107c10")
            self.after(2000, lambda: self.btn_copy.configure(text="📋 CLONE LAST CODE", fg_color="#1a1a1a"))

    def export_chat(self):
        content = self.chat_display.get("0.0", "end")
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f: f.write(content)

    def new_chat(self):
        self.chat_display.configure(state="normal")
        self.chat_display.delete("0.0", "end")
        self.reset_memory()
        self.chat_display.insert("end", f">>> KMATRIX ONLINE | PROTOCOL: {self.current_mode.upper()}\n" + "="*50 + "\n\n")
        self.chat_display.configure(state="disabled")

    def typewriter_effect(self, text, index=0, is_first=True):
        self.chat_display.configure(state="normal")
        if is_first:
            self.chat_display.insert("end", f"\n[KMATRIX] >>> \n")
            self.last_ai_response = text
            threading.Thread(target=self.speak, args=(text,), daemon=True).start()
        
        if index < len(text):
            self.chat_display.insert("end", text[index])
            self.chat_display.see("end")
            self.chat_display.configure(state="disabled")
            self.after(5, self.typewriter_effect, text, index + 1, False)
        else:
            self.chat_display.insert("end", "\n\n" + "-"*60 + "\n\n")
            self.chat_display.configure(state="disabled")
            self.progress_bar.stop()
            self.send_btn.configure(state="normal", text="EXECUTE", fg_color="#0078d4")

    def start_chat_thread(self):
        prompt = self.user_input.get("0.0", "end").strip()
        if not prompt: return
        
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"[USER] >>> \n{prompt}\n\n")
        self.chat_display.configure(state="disabled")
        
        self.user_input.delete("0.0", "end")
        self.send_btn.configure(state="disabled", text="THINKING...", fg_color="#555")
        self.progress_bar.start()

        threading.Thread(target=self.get_ai_response, args=(prompt,), daemon=True).start()

    def get_ai_response(self, prompt):
        try:
            self.chat_history.append({"role": "user", "content": prompt})
            response = self.client.chat.completions.create(model="gpt-4o-mini", messages=self.chat_history)
            answer = response.choices[0].message.content
            self.chat_history.append({"role": "assistant", "content": answer})
            self.after(0, lambda: self.typewriter_effect(answer))
        except Exception as e:
            self.after(0, lambda: self.progress_bar.stop())
            self.after(0, lambda: self.send_btn.configure(state="normal", text="EXECUTE", fg_color="#0078d4"))

if __name__ == "__main__":
    app = KMatrixAI()
    app.mainloop()