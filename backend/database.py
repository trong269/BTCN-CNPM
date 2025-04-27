# import thư viện
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base  # Sử dụng declarative_base từ sqlalchemy.orm
from sqlalchemy.exc import SQLAlchemyError

'''
create_engine: Hàm này từ SQLAlchemy được sử dụng để thiết lập kết nối với cơ sở dữ liệu
declarative_base: Hàm này tạo ra một lớp cơ sở mà tất cả các models ORM của bạn sẽ kế thừa. Nó là phần cơ bản của mô hình đối tượng quan hệ (ORM).
sessionmaker: Hàm này tạo ra một lớp Session mà bạn sẽ sử dụng để tương tác với cơ sở dữ liệu.
'''

# cấu hình kết nối CSDL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Trongnguyen123@localhost:3306/CNPM"
# tạo engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# tạo SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# tạo base
Base = declarative_base()

def get_db():
    """
    Hàm này tạo ra một phiên làm việc với cơ sở dữ liệu.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def test_connection():
#     try:
#         # Tạo engine
#         engine = create_engine(SQLALCHEMY_DATABASE_URL)
        
#         # Thử kết nối và thực hiện một truy vấn đơn giản
#         with engine.connect() as connection:
#             result = connection.execute(text("SELECT 1"))
#             for row in result:
#                 print(f"Kết nối thành công! Kết quả: {row}")
        
#         # Thử liệt kê các bảng trong database
#         with engine.connect() as connection:
#             result = connection.execute(text("SHOW TABLES"))
#             print("Các bảng trong database CNPM:")
#             for row in result:
#                 print(f"- {row[0]}")
                
#         return True
            
#     except SQLAlchemyError as e:
#         print(f"Lỗi kết nối đến database: {e}")
#         return False

# test_connection()
