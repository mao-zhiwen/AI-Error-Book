from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_PATH

# 连接SQLite数据库
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 定义错题数据表
class ErrorBook(Base):
    __tablename__ = "error_book"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    subject = Column(String(20), index=True)  # 学科
    question = Column(Text)                   # 题目内容
    wrong_answer = Column(Text)               # 错误答案
    correct_answer = Column(Text)             # 正确答案
    ai_analysis = Column(Text)                # AI分析结果
    note = Column(Text)                       # 个人备注

# 自动创建数据表
Base.metadata.create_all(bind=engine)

# 数据库操作函数（和main_app.py里的导入完全对应）
def add_error(subject, question, wrong_answer, correct_answer, ai_analysis, note):
    """添加新错题"""
    db = SessionLocal()
    new_error = ErrorBook(
        subject=subject,
        question=question,
        wrong_answer=wrong_answer,
        correct_answer=correct_answer,
        ai_analysis=ai_analysis,
        note=note
    )
    db.add(new_error)
    db.commit()
    db.close()

def get_all_errors():
    """获取所有错题"""
    db = SessionLocal()
    errors = db.query(ErrorBook).all()
    db.close()
    return errors

def delete_error(error_id):
    """删除指定错题"""
    db = SessionLocal()
    db.query(ErrorBook).filter(ErrorBook.id == error_id).delete()
    db.commit()
    db.close()