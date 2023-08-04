import pytest
from django.urls import reverse
from rest_framework import status

from goals.models import BoardParticipant


@pytest.mark.django_db()
class TestBoardRetrieveView:
    @pytest.fixture(autouse=True)
    def setup(self, board_participant):
        self.url = self.get_url(board_participant.board_id)

    @staticmethod
    def get_url(board_pk: int):
        return reverse('goals:board_details', kwargs={'pk': board_pk})

    def test_auth_required(self, client):
        """
        Неавторизованные пользователи при запросе доски получат ошибку
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_retrieve_deleted_board(self, auth_client, board):
        """
        Ошибка при запросе удаленной доски
        """
        board.is_deleted = True
        board.save()
        response = auth_client.get(self.url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_failed_to_retrieve_foreign_board(self, client, user_factory):
        """
        Авторизованные пользователи при запросе чужой доски получат ошибку
        """
        another_user = user_factory.create()
        client.force_login(another_user)

        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db()
class TestBoardDestroyView:
    @pytest.fixture(autouse=True)
    def setup(self, board_participant):
        self.url = self.get_url(board_participant.board_id)

    @staticmethod
    def get_url(board_pk: int):
        return reverse('goals:board_details', kwargs={'pk': board_pk})

    def test_auth_required_delete_board(self, client, ):
        """
        Неавторизованные пользователи получат ошибку при удалении доски
        """
        response = client.delete(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize('role', [
        BoardParticipant.Role.writer,
        BoardParticipant.Role.reader,
    ], ids=['writer', 'reader']
    )
    def test_not_owner_failed_to_delete_board(self, client, user_factory, board, board_participant_factory, role):
        """
        Авторизованные пользователи получат ошибку при удалении чужой доски
        """
        another_user = user_factory.create()
        board_participant_factory.create(
            user=another_user, board=board,
            role=role
        )
        client.force_login(another_user)
        response = client.delete(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_owner_have_to_delete_board(self, auth_client, board):
        """
        Авторизованные пользователи могут удалять свои доски
        """
        response = auth_client.delete(self.url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        board.refresh_from_db()
        assert board.is_deleted is True
