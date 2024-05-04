import React from 'react';
import {Card, Header, HeaderContent, Icon, Image} from 'semantic-ui-react';

const AboutUs: React.FC = () => {
    const authors = [
        {
            image: '/avatar/large/ade.jpg',
            name: 'John Doe',
            career: 'Software Developer',
            icon: 'user secret'
        },
        {
            image: '/avatar/large/chris.jpg',
            name: 'Jane Smith',
            career: 'Project Manager',
            icon: 'user graduate'
        },
        {
            image: '/avatar/large/elliot.jpg',
            name: 'Alice Johnson',
            career: 'UI/UX Designer',
            icon: 'user ninja'
        },
        {
            image: '/avatar/large/laura.jpg',
            name: 'Bob Brown',
            career: 'DevOps Engineer',
            icon: 'user astronaut'
        }
    ];

    return (
        <div className="about-us-container">
            <Header as="h1" icon textAlign="center">
                <Icon name='users' circular/>
                <HeaderContent>About Us</HeaderContent>
            </Header>
            <div className="cards-container" style={{marginTop: "2em"}}>
                {authors.map((author, index) => (
                    <Card key={index} className="author-card">
                        <Card.Content>
                            <Image
                                floated='right'
                                size='huge'
                                src={author.image}
                            />
                            <Card.Header>{author.name}</Card.Header>
                            <Card.Meta>{author.career}</Card.Meta>
                            <Card.Description>
                                {`${author.name} is a ${author.career.toLowerCase()} at our company.`}
                            </Card.Description>
                        </Card.Content>
                    </Card>
                ))}
            </div>
        </div>
    );
};

export default AboutUs;
