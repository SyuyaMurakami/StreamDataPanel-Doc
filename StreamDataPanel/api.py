import os
import threading
import json
import logging
import atexit
from datetime import datetime
from typing import Optional, Union, Dict, Any, Callable
from .apiCore import WebsocketManager

__all__ = [
    'start_api',
    'restart_api',
    'Line',
    'Bar',
    'Sequence',
    'Lines',
    'Bars',
    'Sequences',
    'Scatter',
    'Area',
    'Areas',
    'Pie',
    'Radar',
    'Surface',
]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

_manager: Union[WebsocketManager, None] = None

def start_config_load():
    """
    start_config_load() is a function to load WebSocket connection parameters 
    from the configuration file.

    Returns
    -------
    host : str
        The host address for the WebSocket server.
    port : str
        The port number for the WebSocket server.
    route : str
        The route path for the WebSocket service.

    """
    from .configEdit import config_load
    config = config_load()

    host = config['WEBSOCKET_CONFIG']['HOST']
    port = config['WEBSOCKET_CONFIG']['PORT']
    route = config['WEBSOCKET_CONFIG']['ROUTE']

    return host, port, route

def start_config_check(host: Union[str, None], port: Union[str, None], route: Union[str, None]):
    """
    start_config_check() is a function to check and populate WebSocket connection 
    configurations. If any parameter is None, it loads the default value from 
    the configuration file.

    Parameters
    ----------
    host : Union[str, None]
        The user-specified host address. If None, default is loaded.
    port : Union[str, None]
        The user-specified port number. If None, default is loaded.
    route : Union[str, None]
        The user-specified route path. If None, default is loaded.

    Returns
    -------
    host : str
        The final determined host address.
    port : str
        The final determined port number.
    route : str
        The final determined route path.

    """  
    if host is None or port is None or route is None:
        hostDefault, portDefault, routeDefault = start_config_load()
        host = hostDefault if host is None else host
        port = portDefault if port is None else port
        route = routeDefault if route is None else route
    
    return host, port, route

def start_manager(host: str, port: str, route: str):
    """
    start_manager() is a function to initialize and start the global WebsocketManager.
    It creates the server instance, starts its thread, and registers a cleanup 
    operation upon program exit.

    Parameters
    ----------
    host : str
        The host address for the WebSocket server.
    port : str
        The port number for the WebSocket server.
    route : str
        The route path for the WebSocket service.

    Returns
    -------
    _manager : WebsocketManager
        The global WebSocket manager instance.

    """
    global _manager
    
    logging.info("Initializing user API.")
    _manager = WebsocketManager(host=host, port=port, route=route)
    _manager.start_server_thread()
    atexit.register(_manager.stop_server_thread)
    logging.info("User API initialized.")

    return _manager

def start_api(host: Optional[str]=None, port: Optional[str]=None, route: Optional[str]=None):
    """
    start_api() is a function to start the real-time data service API.
    If the service is already running, it returns the current manager instance. 
    Otherwise, it initializes and starts it.

    Parameters
    ----------
    host : Optional[str]
        Optional host address. If None, the default value from the config file is used.
    port : Optional[str]
        Optional port number. If None, the default value from the config file is used.
    route : Optional[str]
        Optional route path. If None, the default value from the config file is used.

    Returns
    -------
    WebsocketManager
        The global WebSocket manager instance.

    """
    global _manager
    
    if _manager is not None:
        logging.info("Data service is already running.")
        return _manager
    else:
        host, port, route = start_config_check(host, port, route)
        return start_manager(host, port, route)

def restart_api(host: Optional[str]=None, port: Optional[str]=None, route: Optional[str]=None):
    """
    restart_api() is a function to restart the real-time data service API.
    If the service is running, it stops the existing service and then restarts it.

    Parameters
    ----------
    host : Optional[str]
        Optional host address. If None, the default value from the config file is used.
    port : Optional[str]
        Optional port number. If None, the default value from the config file is used.
    route : Optional[str]
        Optional route path. If None, the default value from the config file is used.

    Returns
    -------
    WebsocketManager
        The new global WebSocket manager instance after restart.

    """
    global _manager

    if _manager is not None:
        logging.info("Data service is already running, restarting...")
        _manager = None
    else:
        logging.info("Data service is not running, starting...")
    return start_api(host=host, port=port, route=route)


class DataStream:
    """
    Abstract class for data streams, defines the synchronous interface
    that users can call.
    """
    @staticmethod
    def _data_validated(data_payload: Any):
        """
        _data_validated() is a static method to validate if the data payload 
        contains the essential structure keys ('id', 'timestamp', 'value').

        Parameters
        ----------
        data_payload : Any
            The data payload to be validated, typically expected to be a dictionary.

        Returns
        -------
        bool
            Returns True if the payload is a valid dictionary and contains 
            'id', 'timestamp', and 'value' keys, otherwise False.

        """ 
        if (not isinstance(data_payload, dict)) or ("id" not in data_payload) or ("timestamp" not in data_payload) or ("value" not in data_payload):
            return False
        else:
            return True

    @staticmethod
    def _data_validated_number(data_payload: Any):
        """
        _data_validated_number() is a static method to validate the payload structure 
        and ensure the 'value' field is a numerical type.

        Parameters
        ----------
        data_payload : Any
            The data payload to be validated.

        Returns
        -------
        bool
            Returns True if validation passes, otherwise False.

        """    
        from numbers import Number
        if DataStream._data_validated(data_payload) and isinstance(data_payload['value'], Number):
            return True
        else:
            return False

    @staticmethod
    def _data_validated_dict(data_payload: Any):
        """
        _data_validated_dict() is a static method to validate the payload structure 
        and ensure the 'value' field is a dictionary type.

        Parameters
        ----------
        data_payload : Any
            The data payload to be validated.

        Returns
        -------
        bool
            Returns True if validation passes, otherwise False.

        """      
        if DataStream._data_validated(data_payload) and isinstance(data_payload['value'], dict):
            return True
        else:
            return False

    @staticmethod
    def _data_validated_list(data_payload: Any):
        """
        _data_validated_list() is a static method to validate the payload structure 
        and ensure the 'value' field is a list type.

        Parameters
        ----------
        data_payload : Any
            The data payload to be validated.

        Returns
        -------
        bool
            Returns True if validation passes, otherwise False.

        """    

        if DataStream._data_validated(data_payload) and isinstance(data_payload['value'], list):
            return True
        else:
            return False

    @staticmethod
    def _data_validated_coordinate(data_payload: Any):
        """
        _data_validated_coordinate() is a static method to validate the payload structure 
        and ensure the 'value' field is a list of length 2 containing numbers (coordinate).

        Parameters
        ----------
        data_payload : Any
            The data payload to be validated.

        Returns
        -------
        bool
            Returns True if validation passes, otherwise False.

        """    
        from numbers import Number
        if DataStream._data_validated_list(data_payload):
            value = data_payload['value']
            if len(value) == 2:
                x, y = value
                if isinstance(x, Number) and isinstance(y, Number):
                    return True
                else:
                    return False
            else:
                return False 
        else:
            return False

    @staticmethod
    def _data_validated_dimension(data_payload: Any):
        """
        _data_validated_dimension() is a static method to validate the payload structure 
        for single-series chart data (e.g., Area, Pie) format: 
        [[dimension_labels], [numerical_values]].

        Parameters
        ----------
        data_payload : Any
            The data payload to be validated.

        Returns
        -------
        bool
            Returns True if the payload is a list of length 2, where both elements 
            are lists of equal length, otherwise False.

        """
        if DataStream._data_validated_list(data_payload):
            value = data_payload['value']
            if len(value) == 2:
                dimension, num = value
                if isinstance(dimension, list) and isinstance(num, list) and len(dimension) == len(num):
                    return True
                else:
                    return False
            return False
        else:
            return False

    @staticmethod
    def _data_validated_dimensions(data_payload: Any):
        """
        _data_validated_dimensions() is a static method to validate the payload structure 
        for multi-series chart data (e.g., Areas, Radar) format: 
        [[dimension_labels], [series_labels], [numerical_list_of_lists]].

        Parameters
        ----------
        data_payload : Any
            The data payload to be validated.

        Returns
        -------
        bool
            Returns True if the payload is a list of length 3, and the lengths of 
            series labels and numerical lists match, otherwise False.

        """
        if DataStream._data_validated_list(data_payload):
            value = data_payload['value']
            if len(value) == 3:
                dimension, series, num = value
                if isinstance(dimension, list) and isinstance(series, list)  and isinstance(num, list) and len(series) == len(num):
                    return True
                else:
                    return False
            return False
        else:
            return False

    @staticmethod
    def _data_validated_surface(data_payload: Any):
        """
        _data_validated_surface() is a static method to validate the payload structure 
        for 3D Surface chart data format.

        Parameters
        ----------
        data_payload : Any
            The data payload to be validated.

        Returns
        -------
        bool
            Returns True if the payload has length 3 and the dimensions/shape 
            metrics are consistent, otherwise False.

        """
        if DataStream._data_validated_list(data_payload):
            value = data_payload['value']
            if len(value) == 3:
                axis, shape, num = value
                if len(axis) == 3 and len(shape) == 2 and len(num) == shape[0] * shape[1]:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False


    def __init__(self, key_word: str, chart_type: str):
        """
        Constructor for the DataStream class. Initializes the stream's keyword 
        and chart type, and registers itself with the global manager.

        Parameters
        ----------
        key_word : str
            A user-defined keyword used to uniquely identify the data stream.
        chart_type : str
            The corresponding chart type for this data stream (e.g., 'line', 'bars').

        """
        self.key_word = key_word.strip().lower()
        self.chart_type = chart_type
        self.data_key = self._get_data_key()
        
        # Register itself with the backend Manager so it can be identified when the frontend subscribes
        _manager.register_data_stream(self.data_key)
        logging.info(f"Registered new DataStream: {self.chart_type} -> {self.key_word}")

    def _get_data_key(self) -> str:
        """Generates a unique key for the backend Manager to identify the data stream"""
        return f"{self.chart_type}<:>{self.key_word}"

    def update(self, data_payload: Dict[str, Any]):
        """
        update() updates the data stream and triggers a push to connected clients.
        It bridges the synchronous call to the asynchronous Manager, which handles 
        cache updates and WebSocket pushes in the background event loop.

        Parameters
        ----------
        data_payload : Dict[str, Any]
            The data payload dictionary containing 'id', 'timestamp', and 'value'.

        """
        _manager.push_update_sync(self.data_key, data_payload)
        logging.debug(f"Pushed update for {self.chart_type} -> {self.key_word}")

    def get_cached_data(self) -> Union[Dict[str, Any], None]:
        """
        get_cached_data() retrieves the latest cached data for the current data stream.

        Returns
        -------
        Union[Dict[str, Any], None]
            The latest data payload dictionary, or None if no data is cached.

        """
        return _manager.get_cached_data_sync(self.data_key)
    
    def execute(self, logic_func: Callable, *args, **kwargs):
        """
        execute() executes the specified logic function in a background thread.
        This is useful for running time-consuming tasks without blocking the main program.

        Parameters
        ----------
        logic_func : Callable
            The function to be executed in the background thread. The function 
            will receive the current DataStream instance as its first argument.
        *args :
            Positional arguments passed to the logic_func.
        **kwargs :
            Keyword arguments passed to the logic_func.

        """
        def thread_target(stream_instance, func, *func_args, **func_kwargs):
            try:
                func(stream_instance, *func_args, **func_kwargs)
            except Exception as e:
                print(f"Error in background thread: {e}")
            finally:
                print(f"Thread finished.")

        thread = threading.Thread(
            target=thread_target, 
            args=(self, logic_func) + args, 
            kwargs=kwargs,
            daemon=True
        )
        
        thread.start()
        logging.info(f"{self.chart_type}('{self.data_key}') calls {logic_func.__name__} in background (daemon) thread.")

    def fresh(self, data_payload_value: Any):
        """
        fresh() is a convenience function that generates a new data payload 
        (with automatic 'id' and 'timestamp') based on the given value and 
        immediately updates the data stream.

        Parameters
        ----------
        data_payload_value : Any
            The actual data value to be pushed, which populates the 'value' field 
            of the data payload.

        """
        data_payload = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
            "timestamp": datetime.now().isoformat(),
            "value": data_payload_value
        }
        self.update(data_payload)


class Line(DataStream):
    def __init__(self, key_word: str):
        super().__init__(key_word, chart_type='line')

    def update(self, data_payload: Dict[str, Any]):
        """
        update() is the data update function for the Line chart.
        It validates that the 'value' field in the payload is a single number.

        Parameters
        ----------
        data_payload : Dict[str, Any]
            The data payload dictionary. Expected format: 
            {id:xxx, timestamp:xxx, value:some_number}

        """
        if not DataStream._data_validated_number(data_payload):
            logging.error(f"Invalid data update form for "+str(self.chart_type)+' -> '+str(self.key_word)+r". Must be like: {id:xxx, timestamp:xxx, value:some_number}")
        else:
            super().update(data_payload)


class Bar(DataStream):
    def __init__(self, key_word: str):
        super().__init__(key_word, chart_type='bar')

    def update(self, data_payload: Dict[str, Any]):
        """
        update() is the data update function for the Bar chart.
        It validates that the 'value' field in the payload is a single number.

        Parameters
        ----------
        data_payload : Dict[str, Any]
            The data payload dictionary. Expected format: 
            {id:xxx, timestamp:xxx, value:some_number}

        """
        if not DataStream._data_validated_number(data_payload):
            logging.error(f"Invalid data update form for "+str(self.chart_type)+' -> '+str(self.key_word)+r". Must be like: {id:xxx, timestamp:xxx, value:some_number}")
        else:
            super().update(data_payload)

class Sequence(DataStream):
    def __init__(self, key_word: str):
        super().__init__(key_word, chart_type='sequence')
    
    def update(self, data_payload: Dict[str, Any]):
        """
        update() is the data update function for the Sequence chart.
        It validates that the 'value' field in the payload is a single number.

        Parameters
        ----------
        data_payload : Dict[str, Any]
            The data payload dictionary. Expected format: 
            {id:xxx, timestamp:xxx, value:some_number}

        """
        if not DataStream._data_validated_number(data_payload):
            logging.error(f"Invalid data update form for "+str(self.chart_type)+' -> '+str(self.key_word)+r". Must be like: {id:xxx, timestamp:xxx, value:some_number}")
        else:
            super().update(data_payload)

class Lines(DataStream):
    def __init__(self, key_word: str):
        super().__init__(key_word, chart_type='lines')

    def update(self, data_payload: Dict[str, Any]):
        """
        update() is the data update function for the Lines chart (multiple lines).
        It validates that the 'value' field in the payload is a dictionary 
        (containing values for multiple series).

        Parameters
        ----------
        data_payload : Dict[str, Any]
            The data payload dictionary. Expected format: 
            {id:xxx, timestamp:xxx, value:{A:some_number, B:some_number}}

        """
        if not DataStream._data_validated_dict(data_payload):
            logging.error("Invalid data update form for "+str(self.chart_type)+' -> '+str(self.key_word)+r". Must be like: {id:xxx, timestamp:xxx, value:{A:some_number, B:some_number}}.")
        else:
            super().update(data_payload)

class Bars(DataStream):
    def __init__(self, key_word: str):
        super().__init__(key_word, chart_type='bars')
    
    def update(self, data_payload: Dict[str, Any]):
        """
        update() is the data update function for the Bars chart (multiple bar groups).
        It validates that the 'value' field in the payload is a dictionary 
        (containing values for multiple series).

        Parameters
        ----------
        data_payload : Dict[str, Any]
            The data payload dictionary. Expected format: 
            {id:xxx, timestamp:xxx, value:{A:some_number, B:some_number}}

        """
        if not DataStream._data_validated_dict(data_payload):
            logging.error("Invalid data update form for "+str(self.chart_type)+' -> '+str(self.key_word)+r". Must be like: {id:xxx, timestamp:xxx, value:{A:some_number, B:some_number}}.")
        else:
            super().update(data_payload)

class Sequences(DataStream):
    def __init__(self, key_word: str):
        super().__init__(key_word, chart_type='sequences')
    
    def update(self, data_payload: Dict[str, Any]):
        """
        update() is the data update function for the Sequences chart.
        It validates that the 'value' field in the payload is a dictionary 
        (containing values for multiple series).

        Parameters
        ----------
        data_payload : Dict[str, Any]
            The data payload dictionary. Expected format: 
            {id:xxx, timestamp:xxx, value:{A:some_number, B:some_number}}

        """
        if not DataStream._data_validated_dict(data_payload):
            logging.error("Invalid data update form for "+str(self.chart_type)+' -> '+str(self.key_word)+r". Must be like: {id:xxx, timestamp:xxx, value:{A:some_number, B:some_number}}.")
        else:
            super().update(data_payload)

class Scatter(DataStream):
    def __init__(self, key_word: str):
        super().__init__(key_word, chart_type='scatter')

    def update(self, data_payload: Dict[str, Any]):
        """
        update() is the data update function for the Scatter chart.
        It validates that the 'value' field in the payload is a list containing 
        two numbers (coordinate [x, y]).

        Parameters
        ----------
        data_payload : Dict[str, Any]
            The data payload dictionary. Expected format: 
            {id:xxx, timestamp:xxx, value:[some_number, some_number]}

        """
        if not DataStream._data_validated_coordinate(data_payload):
            logging.error("Invalid data update form for "+str(self.chart_type)+' -> '+str(self.key_word)+r". Must be like: {id:xxx, timestamp:xxx, value:[some_number, some_number]}.")
        else:
            super().update(data_payload)

class Area(DataStream):
    def __init__(self, key_word: str):
        super().__init__(key_word, chart_type='area')

    def update(self, data_payload: Dict[str, Any]):
        """
        update() is the data update function for the Area chart.
        It validates the payload against the single-dimension chart data format.

        Parameters
        ----------
        data_payload : Dict[str, Any]
            The data payload dictionary. Expected format is:
            {id:xxx, timestamp:xxx, value:[[A, B, C], [1, 2, 3]]}
            - The first element of 'value' is used as x-axis tickers.
            - The second element of 'value' is a list of numbers, representing 
              the true value at different x-axis tickers.

        """
        if not DataStream._data_validated_dimension(data_payload):
            logging.error("Invalid data update form for "+str(self.chart_type)+' -> '+str(self.key_word)+r". Must be like: {id:xxx, timestamp:xxx, value:[[A, B, C], [1, 2, 3]]}.")
        else:
            super().update(data_payload)

class Areas(DataStream):
    def __init__(self, key_word: str):
        super().__init__(key_word, chart_type='areas')

    def update(self, data_payload: Dict[str, Any]):
        """
        update() is the data update function for the Areas chart (multiple areas).
        It validates the payload against the multi-dimension chart data format.

        Parameters
        ----------
        data_payload : Dict[str, Any]
            The data payload dictionary. Expected format is:
            {id:xxx, timestamp:xxx, value:[[A, B, C], [label_1, label_2], [[1, 2, 3],[4, 5, 6]]]}
            - The first element of 'value' is used as x-axis tickers.
            - The second element of 'value' is the labels for different data series.
            - The third element of 'value' is a 2D array, representing the true 
              values for different data series.

        """
        if not DataStream._data_validated_dimensions(data_payload):
            logging.error("Invalid data update form for "+str(self.chart_type)+' -> '+str(self.key_word)+r". Must be like: {id:xxx, timestamp:xxx, value:[[A, B, C], [label_1, label_2], [[1, 2, 3],[4, 5, 6]]]}.")
        else:
            super().update(data_payload)

class Pie(DataStream):
    def __init__(self, key_word: str):
        super().__init__(key_word, chart_type='pie')
    
    def update(self, data_payload: Dict[str, Any]):
        """
        update() is the data update function for the Pie chart.
        It validates the payload against the single-dimension chart data format 
        (used for labels and corresponding values).

        Parameters
        ----------
        data_payload : Dict[str, Any]
            The data payload dictionary. Expected format is:
            {id:xxx, timestamp:xxx, value:[[A, B, C], [1, 2, 3]]}
            - The first element of 'value' is used as labels (categories).
            - The second element of 'value' is a list of numbers, representing 
              the true value for each label.

        """
        if not DataStream._data_validated_dimension(data_payload):
            logging.error("Invalid data update form for "+str(self.chart_type)+' -> '+str(self.key_word)+r". Must be like: {id:xxx, timestamp:xxx, value:[[A, B, C], [1, 2, 3]]}.")
        else:
            super().update(data_payload)

class Radar(DataStream):
    def __init__(self, key_word: str):
        super().__init__(key_word, chart_type='radar')

    def update(self, data_payload: Dict[str, Any]):
        """
        update() is the data update function for the Radar chart.
        It validates the payload against the radar chart data format.

        Parameters
        ----------
        data_payload : Dict[str, Any]
            The data payload dictionary. Expected format is:
            {id:xxx, timestamp:xxx, value:[[A, B, C], [100, 100, 100], [4, 5, 6]]}
            - The first element of 'value' is used as dimension labels.
            - The second element of 'value' is the max value at different dimensions.
            - The third element of 'value' is a list of numbers, representing 
              the true value at different dimensions.

        """
        if not DataStream._data_validated_dimensions(data_payload):
            logging.error("Invalid data update form for "+str(self.chart_type)+' -> '+str(self.key_word)+r". Must be like: {id:xxx, timestamp:xxx, value:[[A, B, C], [100, 100, 100], [4, 5, 6]]}.")
        else:
            super().update(data_payload)

class Surface(DataStream):
    def __init__(self, key_word: str):
        super().__init__(key_word, chart_type='surface')
    
    def update(self, data_payload: Dict[str, Any]):
        """
        update() is the data update function for the Surface chart (3D).
        It validates the payload against the 3D surface chart data format.

        Parameters
        ----------
        data_payload : Dict[str, Any]
            The data payload dictionary. Expected format is:
            {id:xxx, timestamp:xxx, value:[[A, B, C], [1, 2], [[1.2, 2.2, 9],[3.2, 4.3, 8]]]}
            - The first element of 'value' is [x-axis name, y-axis name, z-axis name].
            - The second element of 'value' is the shape of the value array, e.g., [number of rows, number of columns].
            - The third element of 'value' is a list of coordinates, e.g., [[x1, y1, z1], [x2, y2, z2]...].

        """
        if not DataStream._data_validated_surface(data_payload):
            logging.error("Invalid data update form for "+str(self.chart_type)+' -> '+str(self.key_word)+r". Must be like: {id:xxx, timestamp:xxx, value:[[A, B, C], [1, 2], [[1.2, 2.2, 9],[3.2, 4.3, 8]]]}.")
        else:
            super().update(data_payload)


