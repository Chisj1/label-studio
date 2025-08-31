import importlib.metadata


class _Meta:
    def get(self, key, default=None):
        return '0.0.0'


try:
    importlib.metadata.metadata('label-studio')
except importlib.metadata.PackageNotFoundError:
    importlib.metadata.metadata = lambda name: _Meta()
    importlib.metadata.version = lambda name: '0.0.0'
