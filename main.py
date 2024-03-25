from dotenv import load_dotenv

from repository.cloud_sql_mysql.evaluate_status import EvaluateStatusRepository
from repository.cloud_sql_mysql.user import UserRepository

if __name__=="__main__":
    load_dotenv('.env')
    # UserExecuteRepository().findCountByUserName(
    #     'GuestUser',
    #     db=next(get_db())
    # )
    #
    # UserExecuteRepository().upsert(user_name='GuestUser',
    #                                db=next(get_db()))
    #
    # all_data = EvaluateStatusRepository().exportAll()
    # print(all_data)

    # regist = UserRepository().register(
    #     user_name='test',password='tsss'
    # )
    login = UserRepository().login(
        user_name='test',password='tsss'
    )
    print(login)