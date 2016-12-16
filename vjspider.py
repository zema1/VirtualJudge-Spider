# coding=utf-8

import json
import os
import time
import sys
import aiohttp
import asyncio

USERNAME = 'test'
PASSWD = 'test'


LOGIN = 'https://vjudge.net/user/login'
ACCEPT = 'https://vjudge.net/status/data/'
SOURCE = 'https://vjudge.net/solution/data/{0}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:48.0) \
                    Gecko/20100101 Firefox/48.0',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest'
}
Ac_data = """draw=1&columns[0][data]=0&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=false&\
columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=1&columns[1][name]=&columns[1][searchable]=true&\
columns[1][orderable]=false&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=2&columns[2][name]=&\
columns[2][searchable]=true&columns[2][orderable]=false&columns[2][search][value]=&columns[2][search][regex]=false&\
columns[3][data]=3&columns[3][name]=&columns[3][searchable]=true&columns[3][orderable]=false&columns[3][search][value]=&\
columns[3][search][regex]=false&columns[4][data]=4&columns[4][name]=&columns[4][searchable]=true&columns[4][orderable]=false&\
columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=5&columns[5][name]=&columns[5][searchable]=true&\
columns[5][orderable]=false&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=6&columns[6][name]=&\
columns[6][searchable]=true&columns[6][orderable]=false&columns[6][search][value]=&columns[6][search][regex]=false&\
columns[7][data]=7&columns[7][name]=&columns[7][searchable]=true&columns[7][orderable]=false&columns[7][search][value]=&\
columns[7][search][regex]=false&columns[8][data]=8&columns[8][name]=&columns[8][searchable]=true&columns[8][orderable]=false&\
columns[8][search][value]=&columns[8][search][regex]=false&start={start}&length=20&search[value]=&search[regex]=false&un=&\
num=-&res=1&language=&inContest=true&contestId={id}"""


class VJSpider(object):

    def __init__(self, loop, uname, passwd):
        self.login_data = 'username=%s&password=%s' % (uname, passwd)
        self.tasks = []
        self.conn = aiohttp.TCPConnector(verify_ssl=False)
        self.session = aiohttp.ClientSession(loop=loop,
                                             headers=headers,
                                             connector=self.conn)

    async def login(self):
        async with self.session.post(LOGIN, data=self.login_data) as resp:
            assert resp.status == 200
            res = await resp.text()
            assert res == u"success"
            print(u"登录成功")

    async def get_accepted(self, contest_id):
        t_headers = headers.copy()
        t_headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        time_flag = str(int(time.time()))[-6:]
        dirname = r'Output_%s_%s' % (contest_id, time_flag)
        os.mkdir(dirname)
        os.chdir(dirname)
        print(u'本次结果保存在%s\n' % dirname)
        for start in range(0, 2000, 20):
            data = Ac_data.format(start=start, id=contest_id)
            async with self.session.post(ACCEPT, data=data, headers=t_headers) as resp:
                res = await resp.text()
            res = json.loads(res)['data']
            if not res:
                break
            self.tasks.extend(res)

        await asyncio.wait([self.__get_code(x) for x in self.tasks])
        self.session.close()

    async def __get_code(self, x):
        run_id = x['runId']
        username = x['userName']
        content_num = x['contestNum']
        async with self.session.post(SOURCE.format(run_id)) as resp:
            res = await resp.text()

        code = json.loads(res)['code']
        file_name = r'%s_%s.cpp' % (username, content_num)
        with open(file_name, 'wb') as f:
            f.write(code.encode('utf-8'))
        print(u'%s 保存成功' % file_name)

async def main(loop, contest_id):
    v = VJSpider(loop, USERNAME, PASSWD)
    try:
        await v.login()
        await v.get_accepted(contest_id)
    except AssertionError:
        print(u"登录失败，请检查用户名或密码是否正确")
        exit(1)
    except (KeyError):
        print(u"获取列表失败，请检查网络或是否有权限访问该contest")
        exit(1)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Usage: ' + os.path.basename(sys.argv[0]) + ' Contest_id')
        print('Example: ' + os.path.basename(sys.argv[0]) + ' 136571')
        sys.exit()
    else:
        contest_id = sys.argv[1]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop, contest_id))
    loop.close()
