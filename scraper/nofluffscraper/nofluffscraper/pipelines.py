# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import nofluffscraper.sketches as sketches

class NofluffscraperPipeline:
    def process_item(self, item, spider):
        return item

class JustJoinItPipeline:
    def __init__(self):
        self.offers = []
        self.skills_freq = {}
        self.locations = {}

    def process_item(self, item, spider):
        requiredSkills = item['requiredSkills'] or []
        niceToHaveSkills = item['niceToHaveSkills'] or []

        skills = list(set(requiredSkills + niceToHaveSkills))

        item['skills'] = skills

        self.offers.append(item)

        self.locations[item['city']] = self.locations.get(item['city'], 0) + 1

        for skill in skills:
            self.skills_freq[skill] = self.skills_freq.get(skill, 0) + 1

        return None

    def close_spider(self, spider):
        top_skills = sorted(self.skills_freq.items(), key=lambda item: item[1], reverse=True)[:100]
        top_locations = sorted(self.locations.items(), key=lambda item: item[1], reverse=True)[:11]

        top_offers = [offer for offer in self.offers]
        with open('skills.txt', 'w') as f:
            for skill, freq in top_skills:
                f.write(f"{skill}: {freq}\n")

        datastream = sketches.DataStream(2, 2)
        skillTags = { skill[0] : datastream.getOrAddTagId(skill[0], "Required skill") for skill in top_skills }
        locationTags = { location[0] : datastream.getOrAddTagId(location[0], "Required Location") for location in top_locations }

        for offer in top_offers:
            offerHash = int(hash(offer['slug']))
            tags = [skillTags[skill] for skill in offer['skills'] if skill in skillTags.keys()]
            datastream.addData(sketches.DataPoint(offerHash,tags))  

            loctags = [locationTags[location] for location in offer['city'] if location in locationTags.keys()]
            datastream.addData(sketches.DataPoint(offerHash,loctags))


        datastream.saveStream()      
