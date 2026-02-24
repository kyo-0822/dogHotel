import pymysql

DB_CONFIG = dict(
    host="localhost",
    user="root",
    password="0000",
    database="dogHotel",
    charset="utf8"
)

class DB:
    def __init__(self, **config):
        self.config = config

    def connect(self):
        return pymysql.connect(**self.config)

    # 로그인
    def login(self, email, password):
        sql = "select count(*) from user_db where email=%s and password=%s"
        try :
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (email, password))
                    count, = cur.fetchone()
                    if count == 1:
                        print("[시스템] 로그인 성공")
                        return True
                    else :
                        print("[시스템] 로그인 실패 : 정보 불일치")
                        return False
        except Exception as e :
            print(f'[시스템] 로그인 오류 발생 {e}')
            return False
    
    # 회원가입
    def signup(self, name, email, password):
        sql = "insert into user_db (name, email, password) values (%s, %s, %s)"
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (name, email, password))
                conn.commit()
                return True
        except Exception as e:
            print(f"[시스템] 회원가입 오류 발생 : {e}")
            return False
        
    # 회원 삭제
    def delete(self, email):
        sql = "delete from user_db where email = %s"
        try :
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (email,))

                    if cur.rowcount > 0:
                        conn.commit()
                        print(f'[시스템] 회원 삭제 성공 : {email}')
                        return True
                    else:
                        print('[시스템] 회원 삭제 실패 : 정보 없음')
                        return False
        except Exception as e :
            print(f'[시스템] 회원 삭제 오류 발생 : {e}')
            return False
            
    # 방 정보 조회
    def room_info(self):
        sql = "select room_num, state from room_info ORDER BY room_num"
        try :
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    result = cur.fetchall()
                    # 객실 상태 반환 ( 객실 정보 윈도우에 출력 )
                    return result
        except Exception as e :
            print(f'[시스템] 객실 상태 조회중 오류 발생 {e}')
            return []

db = DB(**DB_CONFIG)