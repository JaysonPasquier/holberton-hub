from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Job, JobApplication
from .serializers import (JobSerializer, JobCreateSerializer, JobApplicationSerializer,
                         JobApplicationCreateSerializer, JobApplicationStatusSerializer)
from .permissions import IsOwnerOrReadOnly, IsJobOwner, IsApplicant

class JobList(generics.ListAPIView):
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'skills_required']
    ordering_fields = ['created_at', 'deadline', 'status']

    def get_queryset(self):
        queryset = super().get_queryset()
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset

class JobDetail(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class JobCreate(generics.CreateAPIView):
    serializer_class = JobCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class JobUpdate(generics.UpdateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class JobDelete(generics.DestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class JobApplicationList(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsJobOwner]

    def get_queryset(self):
        job_id = self.kwargs.get('pk')
        return JobApplication.objects.filter(job_id=job_id)

    def get_job(self):
        return get_object_or_404(Job, id=self.kwargs.get('pk'))

    def check_object_permissions(self, request, obj):
        # Pass the job to the permission class
        job = self.get_job()
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, job):
                self.permission_denied(request)

class JobApplicationCreate(generics.CreateAPIView):
    serializer_class = JobApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404(Job, id=job_id)

        # Check if the user has already applied
        if JobApplication.objects.filter(job=job, applicant=request.user).exists():
            return Response(
                {"detail": "You have already applied for this job."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if user is the job creator
        if job.created_by == request.user:
            return Response(
                {"detail": "You cannot apply to your own job posting."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if job is still open
        if job.status != 'open':
            return Response(
                {"detail": "This job is no longer accepting applications."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(job=job, applicant=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class JobApplicationDetail(generics.RetrieveAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsJobOwner|IsApplicant]

class JobApplicationStatusUpdate(generics.UpdateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationStatusSerializer
    permission_classes = [permissions.IsAuthenticated, IsJobOwner]
