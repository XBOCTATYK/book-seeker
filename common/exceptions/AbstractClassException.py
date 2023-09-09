class AbstractClassException(RuntimeError):
    subject = None

    def __init__(self, subject, *args):
        self.subject = subject
        super().__init__(*args)

