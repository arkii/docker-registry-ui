#-*- coding:utf8 -*-

#全局配置端
GLOBAL={

    "Host": "0.0.0.0",
    #Application run network address, you can set it `0.0.0.0`, `127.0.0.1`, ``, `None`;
    #Default run on all network interfaces.

    "Port": 10060,
    #Application run port, default port;

    "LogLevel": "DEBUG",
    #应用程序写日志级别，目前有DEBUG，INFO，WARNING，ERROR，CRITICAL
}

#生产环境配置段
PRODUCT={

    "ProcessName": "SIC.RegistryUI",
    #Custom process, you can see it with "ps aux|grep ProcessName".

    "ProductType": "tornado",
    #生产环境启动方法，可选`gevent`, `tornado`, `uwsgi`,其中tornado log level是WARNNING，也就是低于WARN级别的日志不会打印或写入日志中。
}
