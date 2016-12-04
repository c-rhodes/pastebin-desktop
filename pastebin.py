#!/usr/bin/python3

import urllib.parse
import urllib.error
import webbrowser
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from socket import timeout
from urllib.request import urlopen

class Pastebin(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.pack(fill=BOTH, expand=1)
        self.api_dev_key = "e60fc685edf45059136f6e6cadc32566"
        self.api_user_key = ""
        self.bad_api_request = "Bad API request"
        self.base_url = "http://pastebin.com/api/"

        self.logged_in = False
        self.logged_in_base_str = "Logged in as "

        self.bind_class("Text", "<Control-a>", self.selectall)

        self.initUI()

    def selectall(self, event):
        event.widget.tag_add("sel", "1.0", "end")

    def initUI(self):
        self.master.title("Pastebin for Desktop")
        self.master.iconbitmap("icon.ico")
        self.master.resizable(FALSE, FALSE)

        ### frames ###
        self.frame    = ttk.Frame(self, padding="3")
        self.topbar   = ttk.Frame(self.frame, padding="2")
        self.content  = ttk.Frame(self.frame, padding="2")
        self.loginbar = ttk.Frame(self.frame, padding="2")
        self.loggedin = ttk.Frame(self.frame, padding="2")
    
        ### frames geometry ###
        self.frame.grid(row=1, column=0, sticky=(N, E, S, W))
        self.topbar.grid(row=0, column=0, columnspan=6, sticky=W)
        self.content.grid(row=1, column=0, columnspan=6, sticky=(N, E, S, W))
        self.loginbar.grid(row=2, column=0, sticky=(N, E, S, W))
        self.loggedin.grid(row=3, column=0, sticky=(N, E, S, W))

        ### textvariables ###
        self.username = StringVar()	# username entry
        self.password = StringVar()	# password entry
        self.exposure = StringVar()	# exposure combobox
        self.expiration = StringVar() 	# expiration combobox
        self.pastetitle = StringVar()	# pastetitle entry
        self.post_result = StringVar()	# label that display submission attempt
        self.logged_in_as = StringVar() # logged in as label
        self.logged_in_as.set(self.logged_in_base_str + "Guest")

        ### topbar widgets ###
        label_newpaste = ttk.Label(self.topbar, text="New Paste", font=("TkHeadingFont", 14))
        label_pastetitle = ttk.Label(self.topbar, text="Paste Title", font="TkFixedFont")
        label_expiration = ttk.Label(self.topbar, text="Expiration", font="TkFixedFont")
        label_exposure = ttk.Label(self.topbar, text="Paste Exposure", font="TkFixedFont")

        self.button_mypastebin = ttk.Button(self.topbar, text="My Pastebin", command=self.mypastebin)

        self.entry_pastetitle = ttk.Entry(self.topbar, textvariable=self.pastetitle)
    
        self.combobox_exposure = ttk.Combobox(self.topbar, textvariable=self.exposure, state="readonly")
        self.combobox_expiration = ttk.Combobox(self.topbar, textvariable=self.expiration, state="readonly")

        self.combobox_exposure["values"] = ("Public", "Unlisted", "Private")
        self.combobox_expiration["values"] = ("Never", "10 Minutes", "1 Hour", "1 Day", "1 Week", "2 Weeks", "1 Month")

        self.combobox_exposure.set("Public")
        self.combobox_expiration.set("Never")
    
        separator_one = ttk.Separator(self.topbar, orient=HORIZONTAL)
            
        ### topbar geometry ###	
        label_newpaste.grid(row=0, column=0, sticky=W)
        label_pastetitle.grid(row=2, column=0, sticky=W)
        label_exposure.grid(row=2, column=2, sticky=W)
        label_expiration.grid(row=2, column=4, sticky=W)

        self.button_mypastebin.grid(row=0, column=5, sticky=E)		

        self.entry_pastetitle.grid(row=2, column=1, sticky=W)
        self.combobox_exposure.grid(row=2, column=3, sticky=W)
        self.combobox_expiration.grid(row=2, column=5, sticky=W)

        separator_one.grid(row=1, column=0, columnspan=6, sticky=(W, E))

        for child in self.topbar.winfo_children(): child.grid_configure(padx=5, pady=5)

        ### content widgets ###
        scrollbar_text = ttk.Scrollbar(self.content)
        self.text_paste = Text(self.content, yscrollcommand=scrollbar_text.set)
        scrollbar_text.config(command=self.text_paste.yview)
        self.button_submit = ttk.Button(self.content, text="Submit", command=self.paste)
        self.label_submit = ttk.Label(self.content, textvariable=self.post_result, font="TkSmallCaptionFont")

        self.text_paste.focus()

        ### content geometry ###
    
        self.text_paste.grid(row=0, column=0, columnspan=3, sticky=(N, E, S, W))
        scrollbar_text.grid(row=0, column=3, sticky=(N, S))
        self.button_submit.grid(row=1, column=0, sticky=W)

        for child in self.content.winfo_children(): child.grid_configure(padx=5, pady=3)
        self.label_submit.grid_forget()

        ### loginbar widgets ###
        self.label_username = ttk.Label(self.loginbar, text="Username", font="TkFixedFont")
        self.label_password = ttk.Label(self.loginbar, text="Password", font="TkFixedFont")
    
        self.entry_username = ttk.Entry(self.loginbar, textvariable=self.username)
        self.entry_password = ttk.Entry(self.loginbar, textvariable=self.password, show="*") 
    
        self.button_login = ttk.Button(self.loginbar, text="Login", command=self.login)

        
    
    
        ### loginbar geometry ### 
    
        self.label_username.grid(row=0, column=0, sticky=W)
        self.label_password.grid(row=1, column=0, sticky=W)

        self.entry_username.grid(row=0, column=1, sticky=W)
        self.entry_password.grid(row=1, column=1, sticky=W)

        self.button_login.grid(row=2, column=1, sticky=W)	

        for child in self.loginbar.winfo_children(): child.grid_configure(padx=5, pady=5)
    
        ### loggedin widgets ###
        self.button_logout = ttk.Button(self.loggedin, text="Logout", command=self.logout)
        label_user = ttk.Label(self.loggedin, textvariable=self.logged_in_as, font="TkSmallCaptionFont")

        ### loggedin geometry ###
    
        self.button_logout.grid()
        label_user.grid(row=0, column=0, sticky=W)
    
        for child in self.loggedin.winfo_children(): child.grid_configure(padx=5, pady=5)
        self.button_logout.grid_forget()
            
        ### column & row configurations ###
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.content.rowconfigure(0, weight=1)
        self.content.rowconfigure(1, weight=1)

        self.loggedin.columnconfigure(1, weight=1)
        self.content.columnconfigure(0, weight=1)	# expands logout button to bottom-right corner
        self.frame.columnconfigure(0, weight=1)
    
        self.update()	

    ### pastebin api procedures ###
    def login(self):
        if self.username.get() == "" or self.password.get() == "": 
            self.error("username or password cannot be empty.")
            return

        api_user_pass_vars = {
                "api_dev_key": self.api_dev_key,
                "api_user_name": self.username.get(),
                "api_user_password": self.password.get()
        }
        argv = urllib.parse.urlencode(api_user_pass_vars)
        binary_argv = argv.encode("utf-8")
        try:	
            request = urllib.request.urlopen(self.base_url + "/api_login.php", binary_argv, timeout=10).read().decode("utf=8")
            if request.startswith(self.bad_api_request): 
                self.error(request)
                return 
            else: 
                self.api_user_key = request
                self.logged_in_as.set(self.logged_in_base_str + self.username.get())

                self.loginbar.grid_forget()

                self.button_logout.grid(row=0, column=1, sticky=E)
                self.logged_in = True

        except (urllib.error.HTTPError, urllib.error.URLError) as error:
            self.error("Failed to connect to pastebin.com, check your connection")
            return
        except timeout:
            self.error("Socket timed out, check your connection.")
            return

    def logout(self):
        self.api_user_key = ""
        self.username.set("")
        self.password.set("")
        self.logged_in_as.set(self.logged_in_base_str + "Guest")
        
        self.button_logout.grid_forget()
        self.loginbar.grid(row=2, column=0, sticky=W)
        self.logged_in = False

    def paste(self):
        if len(self.text_paste.get(1.0, END)) == 1:
            self.error("Text box must contain content.")
            return

        api_expiry_dates = ["N", "10M", "1H", "1D", "1W", "2W", "1M"]

        pastebin_vars = {
                "api_dev_key": self.api_dev_key,
                "api_option": "paste",
                "api_paste_name": self.entry_pastetitle.get(),
                "api_paste_code": self.text_paste.get(1.0, END),
                "api_paste_private": self.combobox_exposure.current(),
                "api_paste_expire_date": api_expiry_dates[self.combobox_expiration.current()]
        }
            
        if self.logged_in: 
            pastebin_vars["api_user_key"] = self.api_user_key

        argv = urllib.parse.urlencode(pastebin_vars)
        binary_argv = argv.encode("utf-8")		

        try:
            request = urllib.request.urlopen(self.base_url + "/api_post.php", binary_argv).read().decode("utf=8")
            if not request.startswith("http://pastebin.com/"): 
                self.error(request)
                return
            else: 
                self.post_result.set("Post successful")
                self.combobox_exposure.set("Public")		# reset combobox
                self.combobox_expiration.set("Never")		# reset combobox
                self.text_paste.delete(1.0, END)		# refresh textbox
                self.entry_pastetitle.delete(0, END)            # refresh entry box
                self.label_submit.grid(row=1, column=1, sticky=W)
                self.label_submit.after(5000, lambda: self.label_submit.grid_forget())	# display message for 5 seconds
                self.notify(request, title="Pastebin uploaded.")

        except (urllib.error.HTTPError, urllib.error.URLError) as error:
            self.error("Failed to connect to pastebin.com, check your connection")
        except timeout:
            self.error("Socket timed out, check your connection.")

    def mypastebin(self):
        if not self.logged_in:
            self.notify("You must be logged in to access your Pastebin.")
            return

        webbrowser.open("http://pastebin.com/u/" + self.username.get())

    def copyToBoard(self, window, message):
        window.clipboard_clear()
        window.clipboard_append(message)
    
    def notify(self, message, title="Message"):
        notificationWindow=Tk()
        notificationWindow.title(title)
        notificationWindow.iconbitmap("icon.ico")
        text=Label(notificationWindow, text=message, pady=10)
        copyToClipboardBtn = Button(notificationWindow, text="Copy to clipboard", command=lambda:self.copyToBoard(notificationWindow, message))
        exitBtn = Button(notificationWindow, text="Ok", command=notificationWindow.destroy)
        text.grid(row=0, column=0, columnspan=2)
        copyToClipboardBtn.grid(row=1, column=0)
        exitBtn.grid(row=1, column=1)

    def error(self, message):
        messagebox.showinfo(message=message, icon="error")

	
def main():	
	pastebin_app = Pastebin()
	pastebin_app.mainloop()

if __name__ == "__main__":
	main()
