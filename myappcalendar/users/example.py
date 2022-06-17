import json

from rest_framework import serializers

class CommentSerializer(serializers.Serializer):
    # initialize fields
    email = serializers.EmailField()
    text = serializers.CharField(max_length = 200)
    is_active = serializers.BooleanField()

class Comment(object):
    def __init__(self, email, text, is_active):
        self.email = email
        self.text = text
        self.is_active = is_active

comment = Comment(email='leila@example.com', text='foo bar', is_active=False)
serializer = CommentSerializer(comment) # object - > orderdict
#serializer = CommentSerializer(data=comment) # json - > python dict
#serializer.is_valid()
print(serializer.validated_data)