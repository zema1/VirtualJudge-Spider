# VirtualJudge Spider

一个简易的`Vjudge`AC源码爬取脚本，可以简单而迅速的爬取某个Contest的所有AC代码并保存在本地。

脚本基于Python3.5+ 异步编程，效率很高



## 用法

首先你需要把clone下来或者直接复制下vjspider.py到本地

+ 依赖库安装

  ```sh
  pip install aiohttp
  ```

+ 修改用户名密码

  修改`vjspider.py`中的`USERNAME`和`PASSWD`改为自己**管理员账号和密码**

  因为只有管理员才有权限查看某个`Contest`的任何人源码

+ 使用方法

  ```sh
  # contest_id 可以从Contest的URL中获取
  python3 vjspider.py [contest_id]
  ```

  ![contest_id](id.png)

  例子：

  ```sh
  python3 vjspider.py 136571
  ```
  如果觉得还不错， 给个star吧~
