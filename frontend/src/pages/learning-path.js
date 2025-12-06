import React from 'react';
import Layout from '@theme/Layout';
import LearningPath from '../theme/LearningPath';

const LearningPathPage = () => {
  return (
    <Layout
      title="Learning Path"
      description="Weekly learning path for the AI Powered Book">
      <main>
        <LearningPath />
      </main>
    </Layout>
  );
};

export default LearningPathPage;
