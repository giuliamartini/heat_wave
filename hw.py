
class HeatWave:
    """classe che categorizza le ondate di calore in
     base alle caratteristiche di lunghezza,temperatura massima, magnitudo e intensità"""

    def __init__(self, events, properties):
        # gli events sono le giornate con valore di temperatura oltre il 95 percentile
        self.events = events
        self.properties = properties
        


