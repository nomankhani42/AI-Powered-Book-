import React from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

const LearningPath = () => {
  const {siteConfig, siteMetadata, globalData} = useDocusaurusContext();

  const allDocs = globalData['docusaurus-plugin-content-docs']?.default?.versions[0]?.docs;

  const learningPathByWeek = {};

  if (allDocs) {
    allDocs.forEach(doc => {
      if (doc.frontMatter && doc.frontMatter.week) {
        const week = doc.frontMatter.week;
        if (!learningPathByWeek[week]) {
          learningPathByWeek[week] = [];
        }
        learningPathByWeek[week].push({
          title: doc.title,
          permalink: doc.permalink,
        });
      }
    });
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h2 className="text-3xl font-bold mb-6 text-primary">Weekly Learning Path</h2>
      {Object.keys(learningPathByWeek).sort((a, b) => parseInt(a) - parseInt(b)).map(week => (
        <div key={week} className="mb-8 p-6 bg-white shadow-lg rounded-lg">
          <h3 className="text-2xl font-semibold mb-4 text-secondary">Week {week}</h3>
          <ul className="list-disc pl-5 space-y-2">
            {learningPathByWeek[week].map((chapter, index) => (
              <li key={index} className="text-gray-700">
                <a href={chapter.permalink} className="text-blue-600 hover:underline">
                  {chapter.title}
                </a>
              </li>
            ))}
          </ul>
        </div>
      ))}
      {Object.keys(learningPathByWeek).length === 0 && (
        <p className="text-gray-600 italic">No chapters assigned to a weekly learning path yet. Add 'week: &lt;number&gt;' to your MDX front matter.</p>
      )}
    </div>
  );
};

export default LearningPath;