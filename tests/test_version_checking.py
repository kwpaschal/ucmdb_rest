"""
Unit tests for version checking infrastructure

Tests the core version comparison, normalization, and decorator functionality
without requiring actual UCMDB server connections.
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ucmdb_rest.utils import (
    _normalize_version,
    compare_versions,
    requires_version,
    UCMDBVersionError,
    clear_version_cache
)


class TestVersionNormalization(unittest.TestCase):
    """Test version string normalization"""

    def test_yyyy_mm_format(self):
        """Test YYYY.MM format normalization"""
        self.assertEqual(_normalize_version("2023.05"), (2023, 5, False))
        self.assertEqual(_normalize_version("2023.11"), (2023, 11, False))
        self.assertEqual(_normalize_version("2024.01"), (2024, 1, False))

    def test_yy_q_format(self):
        """Test YY.Q format normalization"""
        # Q1 = January (month 1)
        self.assertEqual(_normalize_version("23.1"), (2023, 1, True))
        # Q2 = April (month 4)
        self.assertEqual(_normalize_version("23.2"), (2023, 4, True))
        # Q3 = July (month 7)
        self.assertEqual(_normalize_version("23.3"), (2023, 7, True))
        # Q4 = October (month 10)
        self.assertEqual(_normalize_version("23.4"), (2023, 10, True))
        self.assertEqual(_normalize_version("24.2"), (2024, 4, True))
        self.assertEqual(_normalize_version("25.4"), (2025, 10, True))


class TestVersionComparison(unittest.TestCase):
    """Test version comparison logic"""

    def test_same_format_comparison(self):
        """Test comparing versions in the same format"""
        # YYYY.MM format
        self.assertTrue(compare_versions("2024.05", "2023.05"))
        self.assertTrue(compare_versions("2023.11", "2023.05"))
        self.assertTrue(compare_versions("2023.05", "2023.05"))
        self.assertFalse(compare_versions("2023.05", "2023.11"))

        # YY.Q format
        self.assertTrue(compare_versions("24.2", "23.4"))
        self.assertTrue(compare_versions("23.4", "23.2"))
        self.assertTrue(compare_versions("23.4", "23.4"))
        self.assertFalse(compare_versions("23.2", "23.4"))

    def test_mixed_format_comparison(self):
        """Test comparing versions across different formats"""
        # 2023.05 (May 2023) < 23.4 (Q4 2023 = October 2023)
        self.assertFalse(compare_versions("2023.05", "23.4"))
        self.assertTrue(compare_versions("23.4", "2023.05"))

        # 24.2 (Q2 2024 = April 2024) > 2023.05 (May 2023)
        self.assertTrue(compare_versions("24.2", "2023.05"))
        self.assertFalse(compare_versions("2023.05", "24.2"))

        # 2023.08 (August 2023) < 23.4 (Q4 2023 = October 2023)
        self.assertFalse(compare_versions("2023.08", "23.4"))
        self.assertTrue(compare_versions("23.4", "2023.08"))

    def test_edge_cases(self):
        """Test edge cases in version comparison"""
        # Same month, different formats
        # 23.1 = Q1 2023 = January 2023 = 2023.01 (approximately)
        # Due to tuple comparison with the format flag, these aren't considered equal
        # 23.1 -> (2023, 1, True), 2023.01 -> (2023, 1, False)
        # Since False < True, (2023, 1, False) < (2023, 1, True)
        self.assertTrue(compare_versions("23.1", "2023.01"),
                       "23.1 (quarterly) should be >= 2023.01 (monthly)")
        self.assertFalse(compare_versions("2023.01", "23.1"),
                        "2023.01 (monthly) should be < 23.1 (quarterly) due to format flag")

        # Test versions that are definitely equal
        self.assertTrue(compare_versions("2023.05", "2023.05"))
        self.assertTrue(compare_versions("23.4", "23.4"))


class TestRequiresVersionDecorator(unittest.TestCase):
    """Test the @requires_version decorator"""

    def setUp(self):
        """Clear version cache before each test"""
        clear_version_cache()

    def test_decorator_allows_compatible_version(self):
        """Test that decorator allows execution when version is compatible"""
        @requires_version("23.4")
        def test_function(token, udserver):
            return "success"

        mock_token = {"Authorization": "Bearer test"}
        mock_server = "test-server"

        with patch('ucmdb_rest.utils.getUCMDBVersion') as mock_version:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "fullServerVersion": "11.8.0",
                "contentPackVersion": "25.4"
            }
            mock_version.return_value = mock_response

            result = test_function(mock_token, mock_server)
            self.assertEqual(result, "success")

    def test_decorator_blocks_incompatible_version(self):
        """Test that decorator raises error when version is incompatible"""
        @requires_version("24.2")
        def test_function(token, udserver):
            return "success"

        mock_token = {"Authorization": "Bearer test"}
        mock_server = "test-server"

        with patch('ucmdb_rest.utils.getUCMDBVersion') as mock_version:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "fullServerVersion": "11.7.0",
                "contentPackVersion": "2023.05"
            }
            mock_version.return_value = mock_response

            with self.assertRaises(UCMDBVersionError) as context:
                test_function(mock_token, mock_server)

            self.assertIn("requires UCMDB version 24.2", str(context.exception))
            self.assertIn("2023.05", str(context.exception))

    def test_decorator_caches_version(self):
        """Test that decorator caches version info"""
        @requires_version("23.4")
        def test_function(token, udserver):
            return "success"

        mock_token = {"Authorization": "Bearer test"}
        mock_server = "test-server"

        with patch('ucmdb_rest.utils.getUCMDBVersion') as mock_version:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "fullServerVersion": "11.8.0",
                "contentPackVersion": "25.4"
            }
            mock_version.return_value = mock_response

            # Call twice
            test_function(mock_token, mock_server)
            test_function(mock_token, mock_server)

            # getUCMDBVersion should only be called once (cached)
            self.assertEqual(mock_version.call_count, 1)

    def test_decorator_handles_version_fetch_error(self):
        """Test that decorator handles errors when fetching version gracefully"""
        @requires_version("23.4")
        def test_function(token, udserver):
            return "success"

        mock_token = {"Authorization": "Bearer test"}
        mock_server = "test-server"

        with patch('ucmdb_rest.utils.getUCMDBVersion') as mock_version:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_version.return_value = mock_response

            # The decorator should allow the call to proceed with a warning
            # rather than raising an error
            result = test_function(mock_token, mock_server)
            self.assertEqual(result, "success")


class TestVersionCacheClearing(unittest.TestCase):
    """Test version cache management"""

    def test_clear_cache(self):
        """Test that cache can be cleared"""
        @requires_version("23.4")
        def test_function(token, udserver):
            return "success"

        mock_token = {"Authorization": "Bearer test"}
        mock_server = "test-server"

        with patch('ucmdb_rest.utils.getUCMDBVersion') as mock_version:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "fullServerVersion": "11.8.0",
                "contentPackVersion": "25.4"
            }
            mock_version.return_value = mock_response

            # First call
            test_function(mock_token, mock_server)
            self.assertEqual(mock_version.call_count, 1)

            # Clear cache
            clear_version_cache()

            # Second call should fetch again
            test_function(mock_token, mock_server)
            self.assertEqual(mock_version.call_count, 2)


if __name__ == '__main__':
    unittest.main()
