from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner
        return obj.created_by == request.user

class IsJobOwner(permissions.BasePermission):
    """
    Custom permission to only allow job owner to see/manage applications.
    """
    def has_object_permission(self, request, view, obj):
        # For JobApplicationList view, obj is the Job
        # For JobApplication objects, check the job's owner
        if hasattr(obj, 'created_by'):  # This is a Job
            return obj.created_by == request.user
        elif hasattr(obj, 'job'):  # This is a JobApplication
            return obj.job.created_by == request.user
        return False

class IsApplicant(permissions.BasePermission):
    """
    Custom permission to allow applicants to view their own applications.
    """
    def has_object_permission(self, request, view, obj):
        # Only for JobApplication objects
        if hasattr(obj, 'applicant'):
            return obj.applicant == request.user
        return False
