import random
from locust import task, FastHttpUser


class DocumentAPI(FastHttpUser):
    # @task
    # def new_paragraph(self):
    #     page_ids = [ 41, 42, 43, 44, 45 ]
    #     page_id = page_ids[random.Random().randint(0,4)]
    #     contents = """
    #     "<p>给表单的dependence层级设置一个规则</p><p><br></p><p>目前生产环境使用规则的study：RMC-9805-001</p><p><br></p><p>```</p><p>mustAnswer($Screening.Subject Enrollment.DSPART)&amp;&amp;getContainStrNum(lowercase($Screening.Subject Enrollment.DSPART), 'part 1') &gt; 0</p>"
    #     """
    #     with self.rest("POST", "/document/api/new/paragraph",
    #                    json={"contents": contents, "pageId": page_id, "paragraphType": "FullText"}) as resp:
    #         if resp.js["code"] != 200:
    #             resp.failure(f"error")

    @task
    def get_paragraph(self):
        page_ids = [41, 42, 43, 44, 45]
        page_id = page_ids[random.Random().randint(0, 4)]
        with self.rest("GET", f"/document/api/page?pageId={page_id}") as resp:
            if resp.js["code"] != 200:
                resp.failure(f"error")