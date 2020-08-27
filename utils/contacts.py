"""Provides code for manipulating contact data in the database.

Also provides various methods for verification.
"""

import tkinter as tk
from tkinter import messagebox
from . import user
from . import helper
import sqlite3


conn = sqlite3.connect('material.db')
c = conn.cursor()


class ContactsManagement:
	"""Provides contact management methods, like addition, deletion, view, modify, search.

	Attributes:-
	"""

	def __init__(self, window, frame, tablename):
		self.tablename = tablename
		self.window = window
		self.frame = frame
		self.clicked = tk.IntVar()
		self.clicked.set(0)
		self.draw_contacts_menu()

	def _gen_new_frame(self):
		"""Destroys any existing frame and generates a new one."""
		if self.frame:
			self.frame.destroy()
		self.frame = tk.Frame(master=self.window, bg='#455A64')
		self.frame.pack(expand='True', fill='both')

	def draw_contacts_menu(self):
		"""Draws buttons for calling different methods on screen."""
		self._gen_new_frame()
		helper.create_button(self.frame, text='Show All Contacts', command=self.show_all_contacts).grid()
		helper.create_button(self.frame, text='Add Contact', command=self.add_contact).grid()
		helper.create_button(self.frame, text='Remove Contact', command=self.remove_contact).grid()
		helper.create_button(self.frame, text='Modify Contact', command=self.modify_contact).grid()
		helper.create_button(self.frame, text='Search Contact', command=self.search_contact).grid()

	def show_all_contacts(self):
		"""Shows all contacts for a user, along with the contact count."""
		# The 0th entry in the tuple returned by fetchone contains the count
		self._gen_new_frame()
		contact_count = c.execute(f'SELECT COUNT(*) FROM {self.tablename}').fetchone()[0]
		# First print the contact count
		textbox = tk.Text(self.frame, bg='#455A64', fg='#FFFFFF', height=1)
		textbox.insert(tk.END, f'Contacts count: {contact_count}')
		textbox.grid()
		# Make a textbox for each row
		for name, number, email in c.execute(f'SELECT * FROM {self.tablename}'):
			textbox = tk.Text(master=self.frame, bg='#455A64', fg='#FFFFFF', height=1)
			textbox.insert(tk.END, f'{name} | {number} | {email}')
			textbox.grid()
		else:
			# Go back when button pressed
			btn_go_back = helper.create_button(self.frame, 'Go Back', command=lambda: self.clicked.set(1))
			btn_go_back.grid(column=0, sticky='w')
			btn_go_back.wait_variable(self.clicked)
			self.draw_contacts_menu()


	def add_contact(self):
		pass

	def remove_contact(self):
		pass

	def modify_contact(self):
		pass

	def search_contact(self):
		"""Matches contacts based on name (case insensitive) and prints all matching results."""
		self._gen_new_frame()
		self.clicked.set(0)
		helper.create_label(self.frame, 'Name to be searched: ').grid(row=0, column=0)
		ent_name_key = tk.Entry(master=self.frame)
		ent_name_key.grid(row=0, column=1)
		btn_submit = helper.create_button(self.frame, text='Submit', command=lambda: self.clicked.set(1))
		btn_submit.grid(row=1, column=0)
		# wait until the submit button is clicked to perform match
		btn_submit.wait_variable(self.clicked)
		name_key = ent_name_key.get().lower()

		# If no matches are found, raise error and return
		if c.execute(f'SELECT * FROM {self.tablename} WHERE LOWER(name) = ?', (name_key, )).fetchone() is None:
			tk.messagebox.showerror(title='No matches found', message='No matching contacts were found')
		else:
			self._display_matched_contacts(name_key)
		self.draw_contacts_menu()
			

	def _display_matched_contacts(self, name_key):
		self._gen_new_frame()
		self.clicked.set(0)
		# Print details for every matching contact name
		for name, number, email in c.execute(f'SELECT * FROM {self.tablename} WHERE LOWER(name) = ?', (name_key, )):
			textbox = tk.Text(master=self.frame, bg='#455A64', fg='#FFFFFF', height=1)
			textbox.insert(tk.END, f'{name} | {number} | {email}')
			textbox.grid()
		else:
			# Go back when button pressed
			btn_go_back = helper.create_button(self.frame, 'Go Back', command=lambda: self.clicked.set(1))
			btn_go_back.grid(column=0, sticky='w')
			btn_go_back.wait_variable(self.clicked)