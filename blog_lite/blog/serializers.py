from rest_framework import serializers
from django.db import transaction
from .models import Post, SubPost

class SubPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubPost
        fields = [
            'id',
            'title',
            'body',
            'likes',
            'views_count',
            'post',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'likes',
            'views_count',
            'post',
            'created_at',
            'updated_at'
        ]


class PostSerializer(serializers.ModelSerializer):
    subposts = SubPostSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'body',
            'likes',
            'views_count',
            'author',
            'created_at',
            'updated_at',
            'subposts'
        ]
        read_only_fields = [
            'id',
            'likes',
            'views_count',
            'author',
            'created_at',
            'updated_at'
        ]

    @transaction.atomic
    def create(self, validated_data):
        subposts_data = validated_data.pop('subposts', [])
        post = Post.objects.create(**validated_data)
        for subpost in subposts_data:
            SubPost.objects.create(post=post, **subpost)
        return post

    @transaction.atomic
    def update(self, instance, validated_data):
        subposts_data = validated_data.pop('subposts', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        existing_ids = [sp.id for sp in instance.subposts.all()]
        new_ids = [sp.get('id') for sp in subposts_data if sp.get('id')]

        for sp_id in existing_ids:
            if sp_id not in new_ids:
                SubPost.objects.filter(id=sp_id).delete()

        for subpost in subposts_data:
            if 'id' in subpost and subpost['id'] in existing_ids:
                sp_obj = SubPost.objects.get(id=subpost['id'])
                sp_obj.title = subpost.get('title', sp_obj.title)
                sp_obj.body = subpost.get('body', sp_obj.body)
                sp_obj.save()
            else:
                SubPost.objects.create(post=instance, **subpost)

        return instance