from unittest.mock import patch

import pytest
from app.ml.model_loader import load_model

def test_missing_model_file_raises_error():
    with patch("app.ml.model_loader.MODEL_PATH") as mock_path:
        mock_path.is_file.return_value = False

        with pytest.raises(FileNotFoundError, match="Model not found"):
            load_model()