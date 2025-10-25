Web
============

.. toctree::
   :maxdepth: 4

There are two parts in StreamDataPanel, a **Web App** and a **Data Server**. 

Web App is a user-interact panel developped by Node. It can only be setted or started by **terminal command**. It is a data consumer, used to handle subscription from users.

Terminal Command
^^^^^^^^^^^^^^^^^^^^^^

runSDP
~~~~~~~~~~~~~~~

Use ``runSDP`` to start it. A web should be started automatically.

testSDP
~~~~~~~~~~~~~~~

Use ``testSDP`` to run a simple test. A web will be opened automatically. Type one of the following words below into ``ChartType`` input: 
::

    line
    bar
    sequence
    lines
    bars
    seq
    radar
    scatter
    surface
    area
    areas

Then type ``test`` into ``KeyWord`` input. Click ``Subscribe`` to see if it runs correctly. If You see a chart with data freshed every second, it means success.

showSDP
~~~~~~~~~~~~~~~

Use ``showSDP`` to print current config. It is a json file with 2 layers. By default, it is:
::

    {
        'APP_CONFIG': {
            'WEB_SOCKET': 'ws://localhost:9005/ws', 
            'TITLE': 'Real-Time Data Panel', 
            'CHART_TYPE': 'ChartType', 
            'KEY_WORD': 'KeyWord', 
            'SUBSCRIBE': 'SUBSCRIBE', 
            'FAILED': 'FAILED', 
            'SUCCESS': 'SUCCESS'
         }, 
         'VITE_CONFIG': {
             'PORT': 5173
         }, 
         'EEL_CONFIG': {
             'PORT_DEV': 5174, 
             'PORT': 9001, 
             'SIZE': [800, 600]
         }, 
         'WEBSOCKET_CONFIG': {
             'HOST': 'localhost', 
             'PORT': 9005, 
             'ROUTE': '/ws', 
             'RELOAD': True
         }
    }

``APP_CONFIG`` is used to set Web App, it can change the words which will show on your app, or change the websocket address.　``WEB_SOCKET`` is the most important config here, which is the websocket address of your data API. If you start your API with self-defined port, make sure you change this, too.

``VITE_CONFIG`` is a development config. If you do not need to build your own web app, you can neglect this.

``EEL_CONFIG`` is also important, it defines the port that your web app will be run by. If your web app can not be started, it might be a port conflict and you may want to change ``PORT`` configuration.

``WEBSOCKET_CONFIG`` defines the default port of your python data API. Make sure this configuration is consistant with ``WEB_SOCKET`` of  ``APP_CONFIG`` .

setSDP
~~~~~~~~~~~~~~~

Use ``setSDP key_layer_1 key_layer_2 value`` to set config value.

StreamDataPanel does not use i18n to support multi-languages. If you want to change language, ``APP_CONFIG`` is what you need. For example, to use a Japanese web app, you need to config it as follows:
::

    setSDP APP_CONFIG TITLE タイトル
    setSDP APP_CONFIG CHART_TYPE チャート種類
    setSDP APP_CONFIG KEY_WORD キーワード
    setSDP APP_CONFIG SUBSCRIBE 申し込む
    setSDP APP_CONFIG FAILED 失敗
    setSDP APP_CONFIG SUCCESS 成功

Once you set it, the value will be cached into your disk. Next time you run ``runSDP``, it will apply your configuration.

resetSDP
~~~~~~~~~~~~~~~

Use ``resetSDP`` to reset config content to default value. It is useful if your configuration leads to some troubles.

Page Interaction
^^^^^^^^^^^^^^^^^^^

Title
~~~~~~~~~~~~~~~

Once a web is opened, you can **double click** the title of your web to enter into edit mode. You can rename the page, click elsewhere to quit edit mode.

Button
~~~~~~~~~~~~~~~

Once a web is opened, you will find three buttons at the top. 

**Theme**

This is the button lying on the left. When moving your mouse into it, a tab will be expanded. Click different tab to change the color theme.

**Download**

Download icon lies on the right. It is to download your config, which is your theme, title and subscribed charts. Your configuration will be saved into your web-browser default download path with ``json`` format.

**Upload**

This is to upload a config json file to refresh the whole page. It is useful when you need to monitor a set of data and repeat this action again and again.

Chart
^^^^^^^^^^^^^^^

There are two kinds of charts in StreamDataPanel, Time-series chart and Shortcut chart. 

Timeseries
~~~~~~~~~~~~~~~

Timeseries chart will keep 100 cached data points and show their change in time line. The x-axis will usually have a type of timestamp.

Timesereis charts are:
::

    line
    bar
    sequence
    lines
    bars
    sequences
    scatter

Shortcut
~~~~~~~~~~~~~

Shortcut chart will only cache and show the latest updated data. 

**Notice**: An important difference is that you can double click a shortcut chart to freeze data update, and interact with this chart. This action will not influence the others. When freezed, a shortcut chart can be zoomed-in or zoomed-out or spinned.

Shortcut charts are:
::

    pie
    radar
    surface
    area
    areas


