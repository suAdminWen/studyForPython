python网络爬虫实战。

## 功能：

爬取各大招聘网站python的职位信息，并进行整合。

## 技术路线：

- requests+BeautifulSoup
- python版本3.5


## 目录说明：

|-src
|-|-spider*.py    **不同版本的实现代码，`*`代表重构版本号。**
|-data
|-|-job*.cvs

## 版本说明

---

2017/12/20

0.9：

- 仅实现智联招聘网站中的部分python职位的信息爬取。
- 实现定向爬取，获取职位的基本信息，但是数据中存在脏数据。
- 使用cvs文件保存数据。


---