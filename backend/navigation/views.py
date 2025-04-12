from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
    Category, Building, Room, QRLocation, Route,
    UserProfile, SearchHistory, VisitedLocation,
    Feedback, Notice
)
from .serializers import (
    CategorySerializer, BuildingSerializer, RoomSerializer,
    QRLocationSerializer, RouteSerializer, UserProfileSerializer,
    SearchHistorySerializer, VisitedLocationSerializer,
    FeedbackSerializer, NoticeSerializer,RoomMinimalSerializer, SearchRoomSerializer,BuildingMinimalSerializer,SearchBuildingSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [permissions.AllowAny]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.select_related('building', 'category').all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]


class QRLocationViewSet(viewsets.ModelViewSet):
    queryset = QRLocation.objects.select_related('room', 'room__building', 'room__category').all()
    serializer_class = QRLocationSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        # Enables building full image URL in serializer
        return {'request': self.request}


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related('start_room', 'end_room').all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.select_related('user').prefetch_related('favorites').all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SearchHistoryViewSet(viewsets.ModelViewSet):
    queryset = SearchHistory.objects.select_related('user', 'room').all()
    serializer_class = SearchHistorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VisitedLocationViewSet(viewsets.ModelViewSet):
    queryset = VisitedLocation.objects.select_related('user', 'room').all()
    serializer_class = VisitedLocationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.select_related('user', 'room').all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all().order_by('-created_at')
    serializer_class = NoticeSerializer
    permission_classes = [permissions.AllowAny]


# ✅ Search API (GET: /search/?query=abc)
@api_view(['GET'])
def search_buildings(request):
    query = request.GET.get('query', '')
    buildings = Building.objects.filter(
        Q(name__icontains=query) |
        Q(location__icontains=query)
    )
    serializer = SearchBuildingSerializer(buildings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_rooms(request):
    query = request.GET.get('query', '')
    rooms = Room.objects.filter(
        Q(name__icontains=query) |
        Q(building__name__icontains=query) |
        Q(category__name__icontains=query)
    )
    serializer = SearchRoomSerializer(rooms, many=True)
    return Response(serializer.data)

# ✅ Shortest Path API (GET: /shortest-path/?start_id=1&end_id=5)
@api_view(['GET'])
def get_shortest_path_room(request):
    start_id = request.GET.get('start_id')
    end_id = request.GET.get('end_id')

    if not start_id or not end_id:
        return Response({'error': 'start_id and end_id required'}, status=400)

    try:
        start = Room.objects.get(id=start_id)
        end = Room.objects.get(id=end_id)
    except Room.DoesNotExist:
        return Response({'error': 'Room not found'}, status=404)

    # Simplified shortest path: BFS over direct Routes
    from collections import deque, defaultdict

    graph = defaultdict(list)
    for route in Route.objects.all():
        graph[route.start_room.id].append(route.end_room.id)
        graph[route.end_room.id].append(route.start_room.id)

    visited = set()
    prev = {}
    queue = deque([start.id])
    visited.add(start.id)

    while queue:
        node = queue.popleft()
        if node == end.id:
            break
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                prev[neighbor] = node
                queue.append(neighbor)

    # Reconstruct path
    path_ids = []
    node = end.id
    while node != start.id:
        path_ids.append(node)
        node = prev.get(node)
        if node is None:
            return Response({'error': 'No path found'}, status=404)
    path_ids.append(start.id)
    path_ids.reverse()

    # Return path with coordinates
    rooms = Room.objects.filter(id__in=path_ids)
    serializer = RoomMinimalSerializer(rooms, many=True)
    return Response({'path': serializer.data})
# ..........................................................
@api_view(['GET'])
def get_shortest_path_building(request):
    start_id = request.GET.get('start_id')
    end_id = request.GET.get('end_id')

    if not start_id or not end_id:
        return Response({'error': 'start_id and end_id required'}, status=400)

    try:
        start = Building.objects.get(id=start_id)
        end = Building.objects.get(id=end_id)
    except Building.DoesNotExist:
        return Response({'error': 'Building not found'}, status=404)

    from collections import deque, defaultdict

    # Build graph where nodes are buildings
    graph = defaultdict(list)
    for route in Route.objects.all():
        start_building = route.start_room.building.id
        end_building = route.end_room.building.id
        if end_building != start_building:  # avoid loops within same building
            graph[start_building].append(end_building)
            graph[end_building].append(start_building)

    # BFS to find shortest path
    visited = set()
    prev = {}
    queue = deque([start.id])
    visited.add(start.id)

    while queue:
        node = queue.popleft()
        if node == end.id:
            break
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                prev[neighbor] = node
                queue.append(neighbor)

    # Reconstruct path
    path_ids = []
    node = end.id
    while node != start.id:
        path_ids.append(node)
        node = prev.get(node)
        if node is None:
            return Response({'error': 'No path found'}, status=404)
    path_ids.append(start.id)
    path_ids.reverse()

    buildings = Building.objects.filter(id__in=path_ids)
    serializer = BuildingMinimalSerializer(buildings, many=True)
    return Response({'path': serializer.data})
