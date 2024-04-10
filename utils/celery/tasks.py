import msgpack
from datetime import datetime

# custom
from celery import shared_task
from speedometer.celery import app
from core.models import SensorData


def publish_message_to_room(message: dict, room_name: str) -> None:
    """
    helper function to publish message to room
    """
    
    try:
        with app.producer_pool.acquire(block=True) as producer:
            producer.publish(
                msgpack.packb({
                    "__asgi_group__": room_name,
                    **message
                }),
                exchange="groups",
                content_encoding="binary",
                routing_key=room_name,
                retry=False
            )
    except Exception as e:
        print(f"No client's connected to exchange!")


@shared_task
def load_sensor_speed():
    """
    loads speed data to database
    """

    # NOTE: for data population, assume that the current second, is the speed of device
    speed = datetime.now().second

    sensor_data_instance = SensorData.objects.create(
        speed=speed
    )
    # sebd message to associated room i.e 'sensor'
    publish_message_to_room(
        {
            'type': 'speed.update',
            'message': {
                'speed': sensor_data_instance.speed,
                'timestamp': str(sensor_data_instance.timestamp)
            },
        },
        room_name='sensor'
    )
    print(f'[server] load sensor speed : {speed}')


@app.on_after_finalize.connect
def setup_periodic_task(sender, **kwargs):
    """
    Setup periodic celery task to call `load_sensor_speed` for every 1 second
    """

    sender.add_periodic_task(1.0, load_sensor_speed.s(), name='Every 1 second')