export const chatData = {
  currentUser: {
    id: '1',
    name: 'Richard Sanford',
    avatar: 'https://via.placeholder.com/40/4F46E5/ffffff?text=RS',
    status: 'online'
  },
  users: [
    {
      id: '1',
      name: 'Richard Sanford',
      avatar: 'https://via.placeholder.com/40/4F46E5/ffffff?text=RS',
      lastMessage: 'A random message',
      timestamp: '2:30 PM',
      isActive: false
    },
    {
      id: '2',
      name: 'Carmen Jacobson',
      avatar: 'https://via.placeholder.com/40/10B981/ffffff?text=CJ',
      lastMessage: 'A random message',
      timestamp: '2:45 PM',
      isActive: false
    },
    {
      id: '3',
      name: 'Brown Campbell',
      avatar: 'https://via.placeholder.com/40/F59E0B/ffffff?text=BC',
      lastMessage: 'A random message',
      timestamp: '3:15 PM',
      isActive: false
    },
    {
      id: '4',
      name: 'Enrique Murphy',
      avatar: 'https://via.placeholder.com/40/3B82F6/ffffff?text=EM',
      lastMessage: 'A random message',
      timestamp: '4:20 PM',
      isActive: true
    },
    {
      id: '5',
      name: 'Marco Fernandez',
      avatar: 'https://via.placeholder.com/40/8B5CF6/ffffff?text=MF',
      lastMessage: 'A random message',
      timestamp: '4:45 PM',
      isActive: false
    },
    {
      id: '6',
      name: 'Alison Powell',
      avatar: 'https://via.placeholder.com/40/EF4444/ffffff?text=AP',
      lastMessage: 'A random message',
      timestamp: '5:10 PM',
      isActive: false
    }
  ],
  messages: [
    {
      id: '1',
      senderId: '4',
      text: 'Lorem ipsum is placeholder text commonly used in...',
      timestamp: '2:45 PM',
      type: 'received'
    },
    {
      id: '2',
      senderId: '1',
      text: 'Lorem ipsum is placeholder text commonly used in...',
      timestamp: '2:50 PM',
      type: 'sent'
    },
    {
      id: '3',
      senderId: '1',
      text: 'Lorem ipsum is placeholder text commonly used in...',
      timestamp: '4:30 PM',
      type: 'sent'
    },
    {
      id: '4',
      senderId: '4',
      text: 'https://via.placeholder.com/200x150/6366F1/ffffff?text=Image',
      timestamp: '5:20 PM',
      type: 'received',
      isImage: true
    },
    {
      id: '5',
      senderId: '1',
      text: 'Lorem ipsum is placeholder text commonly used in the graphic, print, and publishing...',
      timestamp: '5:48 PM',
      type: 'sent'
    }
  ]
}; 