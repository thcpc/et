import redis

# 创建 Redis 连接
r = redis.Redis(
    host='localhost',  # Redis 服务器地址
    port=6379,         # Redis 端口
    # password='your_password',  # Redis 密码（如果没有密码，可以省略）
    db=0               # 数据库编号（默认是 0）
)

# 测试连接
try:
    r.ping()
    print("成功连接到 Redis")
except redis.ConnectionError:
    print("无法连接到 Redis")