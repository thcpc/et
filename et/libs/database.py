from sqlalchemy.exc import SQLAlchemyError




def add_record(model_class, **kwargs):
    session = get_session()
    try:
        new_user = model_class(**kwargs)
        session.add(new_user)
        session.commit()  # 确保提交事务
    except SQLAlchemyError as e:  # 捕获所有SQLAlchemy异常并处理它们，例如重试或回滚等。
        session.rollback()  # 如果发生错误，回滚事务以避免数据损坏。
        print("An error occurred:", e)
    finally:
        session.close()  # 确保会话被关闭。
