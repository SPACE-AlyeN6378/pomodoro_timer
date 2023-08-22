from table import Table
import pygame
import time
import threading
from tkinter import messagebox

WORKING_TIME = 0
SHORT_BREAK = 1
LONG_BREAK = 2
light_blue ="#75cfff"

class Pomodoro:
    def split_hours(self, hours):
        # Check whether the number of hours is a positive integer or not
        if not (isinstance(hours, int) and hours > 0):
            raise ValueError("The number of hours must be a positive integer")
        
        # Initialize the variables
        long_break_mins = 15
        num_of_intervals = hours * 2
        extra_minutes = 0
        intervals = []
        index = 0
        cycle_number = 1

        while index < num_of_intervals:
            if (index + 1) % 5 == 0:
                # 15-minute break
                intervals.append((0, 0, long_break_mins))
                extra_minutes += (30 - long_break_mins)

                if extra_minutes >= 30:
                    extra_minutes -= 30
                    num_of_intervals += 1
            else:
                # 25 minutes of work, 5 minutes of short break
                intervals.append((cycle_number, 25, 5))
                cycle_number += 1

            index += 1

        if extra_minutes > 0: intervals.append((cycle_number, extra_minutes, 0))
        if intervals[len(intervals) - 1] == (cycle_number-1, 25, 5):
            intervals[len(intervals) - 1] = (cycle_number-1, 30, 0)

        return tuple(intervals)
    
    def __init__(self, root, hours):
        self.root = root
        self.root.title("Pomodoro Timer")

        self.intervals = self.split_hours(hours)
        self.table = Table(self.root, len(self.intervals))
        self.table.change_text("     ", 2, 0)

        self.paused = False
        self.is_timer_running = False
        self.timer_thread = None

    def play_sound(self, ringtone):
        pygame.mixer.init()
        sound = pygame.mixer.Sound(f"sounds/{ringtone}")
        sound.play()

    def str_format(self, time_in_secs):
        minutes = time_in_secs // 60
        seconds = time_in_secs % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def start_timer(self, seconds, x, y, message, ringtone, alarm_on=True):
        if seconds != 0:
            while (not self.paused) and seconds > 0:
                self.table.change_text(self.str_format(seconds), x, y)
                self.root.update()  # Update the GUI
                self.root.after(1000)  # Delay for 1 second
                seconds -= 1
            
            self.table.change_text(self.str_format(seconds), x, y)
            self.table.change_color(x, y, 'silver')
            self.root.update()  # Update the GUI

            # Ring the alarm!
            if alarm_on:
                self.root.deiconify()
                self.play_sound(ringtone=ringtone)
                messagebox.showinfo("Time's Up!", message=message)


        else:
            self.table.change_color(x, y, 'silver')
            self.table.change_text(self.str_format(seconds), x, y)

        self.is_timer_running = False

    def start_one_cycle(self, row_number):
        cycle_number, working_mins, break_mins = self.intervals[row_number]

        work_fg_color = 'red' if cycle_number != 0 else 'silver'
        break_fg_color = 'green' if cycle_number != 0 else 'blue'
        bg_color = 'white' if cycle_number != 0 else light_blue

        work_ringtone = "to_be_continued.mp3" if row_number == (len(self.intervals) - 1) else "ALERT.WAV"
        break_ringtone = "ding.wav" if cycle_number != 0 else "bell1.wav"
        if row_number == (len(self.intervals) - 1):
            end_of_work_msg = "OUT OF TIME! To be continued..."
        else:
            end_of_work_msg = "Break time!"
        
        allow_ringing = True
        if cycle_number != 0:
            if cycle_number % 4 == 0:
                allow_ringing = False
            
        # Cycle number
        if cycle_number == 0: # Long break
            self.table.change_text("LB", 0, row_number)
            self.table.change_color(0, row_number, bg_color=bg_color)
        else:
            self.table.change_text(cycle_number, 0, row_number)
        
        # Working time
        self.table.change_color(1, row_number, fg_color=work_fg_color)
        self.start_timer(working_mins, 1, row_number, message=end_of_work_msg, 
                         ringtone=work_ringtone)

        # Short Break
        self.table.change_color(2, row_number, fg_color=break_fg_color)
        self.start_timer(break_mins, 2, row_number, message="Get back to work!", 
                         ringtone=break_ringtone, 
                         alarm_on=allow_ringing)
        
        self.table.change_color(1, row_number, fg_color='silver', bg_color=bg_color)
        self.table.change_color(2, row_number, fg_color='silver', bg_color=bg_color)

    def start_pomodoro(self):
        for i in range(len(self.intervals)):
            self.start_one_cycle(i)
