ALTER TABLE posts AUTO_INCREMENT = 1;
ALTER TABLE likes AUTO_INCREMENT = 1;
ALTER TABLE comments AUTO_INCREMENT = 1;

INSERT INTO posts (title, content, image, user_id, created_at, updated_at)
VALUES
    ('Post Title 1', 'This is the content for post 1. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+1', 1, NOW(), NOW()),
    ('Post Title 2', 'This is the content for post 2. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+2', 1, NOW(), NOW()),
    ('Post Title 3', 'This is the content for post 3. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+3', 1, NOW(), NOW()),
    ('Post Title 4', 'This is the content for post 4. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+4', 1, NOW(), NOW()),
    ('Post Title 5', 'This is the content for post 5. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+5', 1, NOW(), NOW()),
    ('Post Title 6', 'This is the content for post 6. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+6', 1, NOW(), NOW()),
    ('Post Title 7', 'This is the content for post 7. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+7', 1, NOW(), NOW()),
    ('Post Title 8', 'This is the content for post 8. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+8', 1, NOW(), NOW()),
    ('Post Title 9', 'This is the content for post 9. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+9', 1, NOW(), NOW()),
    ('Post Title 10', 'This is the content for post 10. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+10', 1, NOW(), NOW()),
    ('Post Title 11', 'This is the content for post 11. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+11', 1, NOW(), NOW()),
    ('Post Title 12', 'This is the content for post 12. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+12', 1, NOW(), NOW()),
    ('Post Title 13', 'This is the content for post 13. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+13', 1, NOW(), NOW()),
    ('Post Title 14', 'This is the content for post 14. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+14', 1, NOW(), NOW()),
    ('Post Title 15', 'This is the content for post 15. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+15', 1, NOW(), NOW()),
    ('Post Title 16', 'This is the content for post 16. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+16', 1, NOW(), NOW()),
    ('Post Title 17', 'This is the content for post 17. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+17', 1, NOW(), NOW()),
    ('Post Title 18', 'This is the content for post 18. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+18', 1, NOW(), NOW()),
    ('Post Title 19', 'This is the content for post 19. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+19', 1, NOW(), NOW()),
    ('Post Title 20', 'This is the content for post 20. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+20', 1, NOW(), NOW()),
    ('Post Title 21', 'This is the content for post 21. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+21', 1, NOW(), NOW()),
    ('Post Title 22', 'This is the content for post 22. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+22', 1, NOW(), NOW()),
    ('Post Title 23', 'This is the content for post 23. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+23', 1, NOW(), NOW()),
    ('Post Title 24', 'This is the content for post 24. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+24', 1, NOW(), NOW()),
    ('Post Title 25', 'This is the content for post 25. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+25', 1, NOW(), NOW()),
    ('Post Title 26', 'This is the content for post 26. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+26', 1, NOW(), NOW()),
    ('Post Title 27', 'This is the content for post 27. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+27', 1, NOW(), NOW()),
    ('Post Title 28', 'This is the content for post 28. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+28', 1, NOW(), NOW()),
    ('Post Title 29', 'This is the content for post 29. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+29', 1, NOW(), NOW()),
    ('Post Title 30', 'This is the content for post 30. It is a placeholder text for the dummy posts.', 'https://via.placeholder.com/150?text=Image+30', 1, NOW(), NOW());
    
INSERT INTO likes (post_id, user_id, created_at)
VALUES
    (1, 1, NOW()),
    (2, 1, NOW()),
    (3, 1, NOW()),
    (4, 1, NOW()),
    (5, 1, NOW()),
    (6, 1, NOW()),
    (7, 1, NOW()),
    (8, 1, NOW()),
    (9, 1, NOW()),
    (10, 1, NOW()),
    (11, 1, NOW()),
    (12, 1, NOW()),
    (13, 1, NOW()),
    (14, 1, NOW()),
    (15, 1, NOW()),
    (16, 1, NOW()),
    (17, 1, NOW()),
    (18, 1, NOW()),
    (19, 1, NOW()),
    (20, 1, NOW());
    
INSERT INTO comments (post_id, user_id, content, created_at)
VALUES
    (1, 1, 'Great post! I really enjoyed reading it.', NOW()),
    (2, 1, 'This is a fantastic article, thanks for sharing.', NOW()),
    (3, 1, 'Interesting perspective on the topic!', NOW()),
    (4, 1, 'I learned something new from this, awesome.', NOW()),
    (5, 1, 'Keep up the good work, looking forward to more posts.', NOW()),
    (6, 1, 'Nice work, this post was really insightful.', NOW()),
    (7, 1, 'I completely agree with your viewpoint on this.', NOW()),
    (8, 1, 'This is very well written, keep it up!', NOW()),
    (9, 1, 'Your research here is very thorough, great job.', NOW()),
    (10, 1, 'I love the clarity in your explanation, thanks for sharing.', NOW()),
    (11, 1, 'This topic is something I’ve been interested in for a while.', NOW()),
    (12, 1, 'Great read, I appreciate the depth of the content.', NOW()),
    (13, 1, 'Looking forward to more posts like this!', NOW()),
    (14, 1, 'I love how you broke this down, makes it easy to understand.', NOW()),
    (15, 1, 'Very insightful post, I learned a lot from it.', NOW()),
    (16, 1, 'Thank you for sharing this information, very useful.', NOW()),
    (17, 1, 'This is a very thought-provoking article.', NOW()),
    (18, 1, 'I really enjoyed this read, great job!', NOW()),
    (19, 1, 'Amazing work, this post has a lot of valuable information.', NOW()),
    (20, 1, 'Very well researched, thanks for putting this together.', NOW());




