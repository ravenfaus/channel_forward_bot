from aiogram.utils.executor import Executor

from bot import dp
from models import base


if __name__ == '__main__':
    runner = Executor(dp)
    base.setup(runner)
    runner.start_polling()
