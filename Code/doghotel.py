import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import QDateTime
from database import db

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UI_path = os.path.join(base_dir, "UI", "doghotel.ui")
from_class = uic.loadUiType(UI_path)[0]

class DogHotel(QMainWindow, from_class):
     def __init__(self):
          super().__init__()
          self.setupUi(self)
          self.db = db
          self.room_dict = {}

          self.init_ui()
          self.load_room()

     def init_ui(self):
          self.start_date_time.setDisplayFormat("yyyy-MM-dd HH:00")
          self.end_date_time.setDisplayFormat("yyyy-MM-dd HH:00")

          now = QDateTime.currentDateTime()
          self.start_date_time.setDateTime(now)
          self.end_date_time.setDateTime(now.addSecs(3600))

          self.room_choice.currentIndexChanged.connect(self.update_status)
          self.reservation.clicked.connect(self.try_reservation)

          self.cancel.clicked.connect(self.cancel_reservation)

     def load_room(self):
          self.room_choice.clear()
          self.room_dict.clear()
          rooms = self.db.room_info()

          for room in rooms:
               room_num = room[0]
               state = room[1]

               self.room_dict[room_num] = state
               self.room_choice.addItem(f"{room_num}번 방", room_num)

          self.update_status()
     
     def update_status(self):
          room_num = self.room_choice.currentData()

          if room_num:
               state = self.room_dict.get(room_num, " ")
               self.status.setText(state)
     
     def try_reservation(self):
          room_num = self.room_choice.currentData()
          if room_num is None:
               return
          
          state = self.room_dict.get(room_num)
          if state == "full":
               QMessageBox.warning(self, "예약 불가", "다른 방을 선택해주세요!")
               return
          
          owner_name_input = self.master_name.text().strip()
          dog_name_input = self.dog_name.text().strip()

          if not owner_name_input or not dog_name_input:
               QMessageBox.warning(self, "입력 오류", "보호자와 강아지 이름을 입력 해주세요")
               return

          start_date = self.start_date_time.dateTime().toString("yyyy-MM-dd HH:00:00")
          end_date = self.end_date_time.dateTime().toString("yyyy-MM-dd HH:00:00")

          try:
               with self.db.connect() as conn:
                    with conn.cursor() as cur:
                         insert_sql = "insert into reservation (room_num, master_name, dog_name, start_date, end_date) values (%s, %s, %s, %s, %s)"
                         cur.execute(insert_sql, (room_num, owner_name_input, dog_name_input, start_date, end_date))

                         update_sql = "update room_info set state = 'full' where room_num = %s"
                         cur.execute(update_sql, (room_num,))
                    
                    conn.commit()
               
               QMessageBox.information(self, "예약 완료", f"{room_num}번 방에 예약이 완료됐습니다.")

               self.master_name.clear()
               self.dog_name.clear()
               self.load_room()

          except Exception as e:
               print(e)
               QMessageBox.critical(self, "DB 오류", "예약 과정에서 오류 발생")

     def cancel_reservation(self):
          room_num = self.room_choice.currentData()
          if room_num is None:
               return
          
          state = self.room_dict.get(room_num)
          if state == "empty":
               QMessageBox.warning(self, "취소 불가", "이미 빈 방입니다")
               return
          
          try:
               with self.db.connect() as conn:
                    with conn.cursor() as cur:
                         delete_sql = "delete from reservation where room_num = %s"
                         cur.execute(delete_sql, (room_num,))

                         update_sql = "update room_info set state = 'empty' where room_num = %s"
                         cur.execute(update_sql, (room_num,))
                    
                    conn.commit()
               
               QMessageBox.information(self, "취소 완료", f"{room_num}번 방의 예약이 취소 됐습니다.")
               self.load_room()
          except Exception as e:
               print(e)
               QMessageBox.critical(self, "DB 오류", "취소 과정에서 오류 발생")