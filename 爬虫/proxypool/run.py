from proxypool.scheduler import Scheduler
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 入口文件 代理池的入口


def main():

    try:
        # 调用Scheduler类的run方法
        s = Scheduler()
        s.run()
    except:
        # 发生异常后进行重试
        main()


if __name__ == '__main__':
    main()
