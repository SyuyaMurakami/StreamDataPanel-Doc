Config
============

.. toctree::
   :maxdepth: 4

This chapter will introduce the way to config StreamDataPanel. 

**Important Notice** : The configuration of StreamDataPanel is cached in your local disk, just in your python package directory. Once you re-install StreamDataPanel, your configuration will be lost. So it is important to open the site-packages directory and save config.json if you want to keep your current configuration. 

Change Web Port
^^^^^^^^^^^^^^^^^^^^^^^

Open your terminal and type the following to change web app port:
::

    setSDP EEL_CONFIG PORT new_port_number

Default port is ``9001`` , if it is occupied, this command will change it to ``new_port_number`` .

**Important Notice** : This port is the ``eel`` port, which means it is only used to start your local-machine web page. It is **not** the communication port between your machine and data server. If you want to run a data generating and pushing service in your machine, this config would be useless.

Change API Port
^^^^^^^^^^^^^^^^^^^^

Open your terminal and type the following to change python API port:
::

    setSDP WEBSOCKET_CONFIG PORT new_port_number

Default port is ``9005`` , if it is occupied, this command will change it to ``new_port_number`` .

This port is used to push data. In the machine where you call ``start_api()`` in your python script, this port will be listened to accept subscription and push data.

**Important Notice** : This port is for your data generating and pushing service. If you have a machine just for open web app and subscribe charts, this config will be useless.

Change Language
^^^^^^^^^^^^^^^^^^^^^^

StreamDataPanel does not use i18n to support multi-languages. If you want to change language, ``APP_CONFIG`` is what you need. For example, to use a Japanese web app, you need to open your terminal and type as follows:
::

    setSDP APP_CONFIG TITLE タイトル
    setSDP APP_CONFIG CHART_TYPE チャート種類
    setSDP APP_CONFIG KEY_WORD キーワード
    setSDP APP_CONFIG SUBSCRIBE 申し込む
    setSDP APP_CONFIG FAILED 失敗
    setSDP APP_CONFIG SUCCESS 成功

Once you set it, the value will be cached into your disk. Next time you run ``runSDP``, it will apply your configuration.

Config Data Server
^^^^^^^^^^^^^^^^^^^^^

The default configuration is designed for local-hosted machine, where a machine will be data generator and data consumer at the same time.

To run your data generation service in one machine and subscribe it from others, you need to change default configuration to allow internet visit:
::

    setSDP WEBSOCKET_CONFIG HOST XXX.XXX.XXX.XXX

``XXX.XXX.XXX.XXX`` should be the ip address of your data service machine.

Config Web APP
^^^^^^^^^^^^^^^^^^^^^

To visit and subscribe charts from another machine, you need to change default configuration:
::

    setSDP APP_CONFIG WEB_SOCKET ws://XXX.XXX.XXX.XXX:new_port/new_route

``XXX.XXX.XXX.XXX`` should be the ip address of your data service machine. ``new_port`` should be the API port of your data service machine. ``new_route`` should be the API route path of your data service machine.

For example, if you run ``showSDP`` in your data service machine, and it prints as:
::

    'WEBSOCKET_CONFIG': {
        'HOST': '192.168.1.178', 
        'PORT': 8619, 
        'ROUTE': '/hello', 
        'RELOAD': True
    }

Make sure to use ``setSDP`` command to change your data comsumption machine:
::

    setSDP APP_CONFIG WEB_SOCKET ws://192.168.1.178:8619/hello

Use ``showSDP`` in data comsumption machine and make sure it is like:
::

    'APP_CONFIG': {
        'WEB_SOCKET': 'ws://192.168.1.178:8619/hello',
        ...
    }

If everything is alright, you should be able to subscribe from one machine to another.
