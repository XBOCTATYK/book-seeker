from apps.analyser.model.RawDataDecodedDto import RawDataDecodedDto


class AbstractProcessor:
    def process(self, dto: RawDataDecodedDto):
        return None
