# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from api_client import APIClient


class FoldersAPI(APIClient):

    def __init__(self, api_server, api_key):
        super().__init__(api_server, api_key)

    def create_root_folder(self, display_name: str) -> int:
        """Create a root folder.

        Args:
            display_name (str): Folder display name.

        Returns:
            int: Folder ID for the new root folder.

        Raises:
            RuntimeError: If the API request failed.
        """
        self.endpoint = f"{self.base_url}/folders/"
        params = {"display_name": display_name}
        response = self.session.post(self.endpoint, json=params)
        if response.status_code == 201:
            return response.json().get('id')
        else:
            raise RuntimeError("Error creating root folder.")

    def create_subfolder(self, folder_id: int, display_name: str) -> int:
        """Create a subfolder within the given folder ID.

        Args:
            folder_id: The ID of the parent folder.
            display_name: The name of the subfolder to check.

        Returns:
            True if the subfolder exists, False otherwise.

        Raises:
            RuntimeError: If the API request failed.
        """
        endpoint = f"{self.base_url}/folders/{folder_id}/folders"
        data = {"display_name": display_name}
        response = self.session.post(endpoint, json=data)
        if response.status_code == 201:
            return response.json().get("id")
        else:
            raise RuntimeError("Error creating subfolder.")

    def folder_exists(self, folder_id: int) -> bool:
        """Checks if a folder with the given ID exists.

        Args:
            folder_id: The ID of the folder to check.

        Returns:
            True if the folder exists, False otherwise.

        Raises:
            RuntimeError: If the API request failed.
        """
        endpoint = f"{self.base_url}/folders/{folder_id}"
        response = self.session.get(endpoint)
        return response.status_code == 200