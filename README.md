# 항해99 테스트

## condition

- [Notion - 항해99 6기(내일배움단, 이월자 대상 문제)](https://teamsparta.notion.site/99-6-1410a5c9c3eb48af8887f283a9e531bc)

## services(~22.03.04 23:59)

- version0 : [http://146.56.187.171:2000](http://146.56.187.171:2000/)
- version1 : [http://146.56.187.171:3000](http://146.56.187.171:3000/)

## versions

- version0 : using MongoDB
- version1 : using json
- version2 : using memory(variables)

## IDE & server

- Visual Studio Code(venv not used)
- Oracle Cloud : Linux(CentOS 8), Docker(compose)

## docker-compose

- version0([http://localhost:2000](http://localhost:2000))

```
$ cd version0
$ docker network create --gateway 172.0.0.1 --subnet 172.0.0.0/16 fmongo
$ docker-compose up -d
```

- version1 or version2([http://localhost:3000](http://localhost:3000))

```
$ cd version1 [or verions2]
$ docker-compose up -d
```
