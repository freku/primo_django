from django.urls import path, include
from blogs.views import PostDelete, PostCreate, PostView, BlogList, BlogView, BlogCreate, BlogEdit, BlogDelete, PostUpdate

app_name = 'blogs'

urlpatterns = [
    path('p/create/<slug:slug>/', PostCreate.as_view(), name='post-create'),
    path('p/<slug:slug>/', include([
        path('', PostView.as_view(), name='post-detail'),
        path('update/', PostUpdate.as_view(), name='post-edit'),
        path('delete/', PostDelete.as_view(), name='post-remove'),
    ])),

    path('b/explore', BlogList.as_view(), name="blogs-explore"),
    path('b/create', BlogCreate.as_view(), name='blog-create'),
    path('b/<slug:slug>/', include([
        path('', BlogView.as_view(), name='view-blog'),
        path('update/', BlogEdit.as_view(), name='blog-edit'),
        path('delete/', BlogDelete.as_view(), name='blog-remove'),
    ])),
]

"""
    explore (blogs, posts), create (blogs, posts)
    b/ : [
        post/ : [
            watch,
            create,
            edit,
            delete
        ],
        blog/ [
            create,
            watch,
        ]
    ]
"""