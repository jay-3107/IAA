import React from 'react';

const Features = () => {
  return (
    <section id="features">
      {/* Flex Container */}
      <div className="container flex flex-col px-4 mx-auto mt-10 space-y-12 md:space-y-0 md:flex-row">
        {/* What's Different */}
        <div className="flex flex-col space-y-12 md:w-1/2">
          <h2 className="max-w-md text-4xl font-bold text-center md:text-left">
          Vision
          </h2>
          <p className="max-w-sm text-center text-darkGrayishBlue md:text-left">
          Becoming a Global Centre of Excellence in various Aviation related Education, Training and Research activities and in the long run to attain Deemed University status imparting Diploma and Degree courses in the Aviation Field as well as becoming an economically independent entity of International Standard.
          </p>
        </div>

        {/* Numbered List */}
        <div className="flex flex-col space-y-8 md:w-1/2">
          {/* List Item 1 */}
          <div className="flex flex-col space-y-3 md:space-y-0 md:space-x-6 md:flex-row">
            {/* Heading */}
            <div className="rounded-l-full bg-brightRedSupLight md:bg-transparent">
              <div className="flex items-center space-x-2">
                <div className="px-4 py-2 text-white rounded-full md:py-1 bg-[#22409A]">
                  01
                </div>
                <h3 className="text-base font-bold md:mb-4 md:hidden">
                ICAO-INDIA Fellowship Programs
                </h3>
              </div>
            </div>

            <div>
              <h3 className="hidden mb-4 text-lg font-bold md:block">
              ICAO-INDIA Fellowship Programs
              </h3>
              <p className="text-darkGrayishBlue">
              To share the expertise of IAA with other countries, IAA has signed a memorandum of Understanding(MoU) with ICAO to offer Fellowship Programs for developing countries at IAA. Under the ICAO-INDIA Developing Countries Training Programs, twenty four fellowships are being offered every year.
              </p>
            </div>
          </div>

          {/* List Item 2 */}
          <div className="flex flex-col space-y-3 md:space-y-0 md:space-x-6 md:flex-row">
            {/* Heading */}
            <div className="rounded-l-full bg-brightRedSupLight md:bg-transparent">
              <div className="flex items-center space-x-2">
                <div className="px-4 py-2 text-white rounded-full md:py-1 bg-[#22409A]">
                  02
                </div>
                <h3 className="text-base font-bold md:mb-4 md:hidden">
                Genesis of Indian Aviation Academy
                </h3>
              </div>
            </div>

            <div>
              <h3 className="hidden mb-4 text-lg font-bold md:block">
              Genesis of Indian Aviation Academy
              </h3>
              <p className="text-darkGrayishBlue">
              It was a historic moment when Memorandum of Understanding (MoU) was signed with Bureau of Civil Aviation Security (BCAS), Director General of Civil Aviation (DGCA) and Airports Authority of India (AAI) to have a joint venture to form a new autonomous body for augmenting the training activities in the Civil Aviation Sector of the Country and also to impart knowledge to other stake holders. A society was formed as National Institute of Aviation Management and Research (NIAMAR-Society) under the Societies Act 1860 on 22nd July,2010. Under the aegis of NIAMAR Society, Indian Aviation Academy has been established.It aims to develop itself as Centre of Excellence in the area of Education,Training and Research in Aviation in Asia Pacific Region.
              </p>
            </div>
          </div>

          {/* List Item 3 */}
          <div className="flex flex-col space-y-3 md:space-y-0 md:space-x-6 md:flex-row">
            {/* Heading */}
            <div className="rounded-l-full bg-brightRedSupLight md:bg-transparent">
              <div className="flex items-center space-x-2">
                <div className="px-4 py-2 text-white rounded-full md:py-1 bg-[#22409A]">
                  03
                </div>
                <h3 className="text-base font-bold md:mb-4 md:hidden">
                IAA wishes you a warm welcome to Indian Aviation Academy
                </h3>
              </div>
            </div>

            <div>
              <h3 className="hidden mb-4 text-lg font-bold md:block">
              IAA wishes you a warm welcome to Indian Aviation Academy
              </h3>
              <p className="text-darkGrayishBlue">
              Indian Aviation Academy (IAA) has constantly endeavoured to empower aviation professionals with knowledge and skill. A full member of ICAO TRAINAIR PLUS PROGRAM (TPP), IAA has collaboration with IATA, ACI,AAAE and many renowned management institutes to foster training activities on global aviation arena. The collaborative pursuit has helped IAA to carve a niche for itself on many national and international platforms. While India is poised to become third largest aviation market in the world very soon, it would require very large pool of trained aviation personnel to meet the industry’s demand. With a team of talented and competent ICAO qualified course developers and instructors, IAA is fully geared up to take on the challenge of bridging the gap between the demand and supply of industry. Having developed five standardized training packages (STPS), the course development unit of IAA is also focusing on upgrading all training packages and benchmarking them in tune with global best practices.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Features;
