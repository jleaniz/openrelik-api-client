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

from openrelik_api_client.api_client import APIClient


class WorkflowsAPI(APIClient):
    def __init__(self, api_server, api_key):
        super().__init__(api_server, api_key)

    def create_workflow(self, folder_id: int, file_ids: list, template_id: int = None) -> int:
        """Creates a new workflow.

        Args:
            folder_id: The ID of the folder to create the workflow in.
            file_ids: A list of file IDs to associate with the workflow.
            template_id: The ID of the workflow template to use.

        Returns:
            The ID of the created workflow.
        """
        endpoint = f"{self.base_url}/folders/{folder_id}/workflows"
        data = {"folder_id": folder_id,
                "file_ids": file_ids, "template_id": template_id}
        response = self.session.post(endpoint, json=data)
        if response.status_code == 200:
            return response.json().get("id")
        raise RuntimeError("Error creating workflow.")

    def get_workflow(self, folder_id: int, workflow_id: int):
        """Retrieves a workflow by ID.

        Args:
            folder_id: The ID of the folder where the workflow exists.
            workflow_id: The ID of the workflow to retrieve.

        Returns:
            The workflow data.
        """
        endpoint = f"{
            self.base_url}/folders/{folder_id}/workflows/{workflow_id}"
        response = self.session.get(endpoint)
        if response.status_code == 200:
            return response.json()

    def update_workflow(self, folder_id: int, workflow_id: int, workflow_data: dict):
        """Updates an existing workflow.

        Args:
            folder_id: The ID of the folder containing the workflow.
            workflow_id: The ID of the workflow to update.
            workflow_data: The updated workflow data.

        Returns:
            The updated workflow data.

        Raises:
            RuntimeError: If the API request failed.
        """
        endpoint = f"{
            self.base_url}/folders/{folder_id}/workflows/{workflow_id}"
        response = self.session.patch(endpoint, json=workflow_data)
        if response.status_code == 200:
            workflow = response.json()
            return workflow
        else:
            raise RuntimeError("Error updating workflow.")

    def delete_workflow(self, folder_id, workflow_id) -> bool:
        """Deletes a workflow.

        Args:
            folder_id: The ID of the folder containing the workflow.
            workflow_id: The ID of the workflow to delete.

        Returns:
            True if the request was successful.

        Raises:
            RuntimeError: If the API request failed.
        """
        endpoint = f"{
            self.base_url}/folders/{folder_id}/workflows/{workflow_id}"
        response = self.session.delete(endpoint)
        return response.status_code == 204

    def run_workflow(self, folder_id: int, workflow_id: int):
        """Runs an existing workflow.

        Args:
            folder_id: The ID of the folder containing the workflow.
            workflow_id: The ID of the workflow to run.
            run_data: Optional data to pass to the workflow run.

        Returns:
            A workflow object.

        Raises:
            RuntimeError: If the API request failed.
        """
        endpoint = f"{
            self.base_url}/folders/{folder_id}/workflows/{workflow_id}/run"
        response = self.session.post(endpoint)
        if response.status_code == 200:
            workflow = response.json()
            return workflow
        else:
            raise RuntimeError("Error running workflow.")
