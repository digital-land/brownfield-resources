import os
import json
import pandas as pd

# points to sample file
data_dir = "data/issues"
organisation_csv = "example-issues.csv"
csv_file_path = os.path.join(data_dir, organisation_csv)


def extractIssueData(issues):
    issues_by_row = {}
    for issue in issues:
        default_field = {issue["field"]: {}}
        issues_by_row.setdefault(issue["row-number"], default_field)
        # print(f'{issue["field"]} : {issue["issue-type"]} : {issue["value"]}')
        issues_by_row[issue["row-number"]].setdefault(issue["field"], {})
        # print(issues_by_row[issue['row-number']][issue['field']])
        issues_by_row[issue["row-number"]][issue["field"]][issue["issue-type"]] = issue[
            "value"
        ]
    return issues_by_row


def mapSingleIssue(field, issue):
    keys = list(issue.keys())
    if "missing" in keys:
        return issue["missing"], "missing", f"No data for {field}"
    elif "enum" in keys:
        return issue["enum"], "invalid", f"Unexpected value for {field}"
    elif "outside England" in keys[0]:
        return issue[keys[0]], "invalid", f"Coordinate provided is outside England"
    elif "minimum" in keys:
        return issue[keys[0]], "invalid", f"Value provided is below the minimum allowed"
    elif "integer" in keys:
        return issue[keys[0]], "invalid", f"Value provided is not a valid number"
    elif "uri" in keys:
        return issue[keys[0]], "invalid", f"Value provided is not a valid URI"
    elif "decimal" in keys:
        return issue[keys[0]], "invalid", f"Unable to recognise coordinate"
    elif "date" in keys:
        return issue[keys[0]], "invalid", f"Date provided is not valid"
    elif "default" in keys:
        if field == "LastUpdatedDate":
            return (
                issue[keys[0]],
                "amended",
                f"No date provided for {field}. Setting to FirstAddedDate",
            )
        elif field == "NetDwellingsRangeTo":
            return (
                issue[keys[0]],
                "amended",
                f"No value provided for {field}. Setting to NetDwellingsRangeFrom",
            )
        elif field == "OrganisationURI":
            return (
                issue[keys[0]],
                "amended",
                f"No value provided for {field}. Setting to default for organisation.",
            )
        elif field == "NetDwellingsRangeFrom":
            return (
                issue[keys[0]],
                "amended",
                f"No value provided for {field}. Using value from deprecated MinNetDwellings column.",
            )
        else:
            return (
                issue[keys[0]],
                "amended",
                f"No value provided for {field}. Setting to a default",
            )
    else:
        return issue[keys[0]], keys[0], "some text"


def generateIssueMessage(field, issues):
    # 'Hectares': {'minimum': '0', 'missing': None}
    # 'SiteReference': {'missing': None}
    # empty defaults to stop it failing
    original = ""
    tag = ""
    message = ""

    issue_types = issues.keys()
    if len(issue_types) > 1:
        # can discount missing (is this done mistakenly?)
        if "missing" in issue_types:
            del issues["missing"]
            original, tag, message = mapSingleIssue(field, issues)
        if "date" in issue_types and "default" in issue_types:
            original = issues["date"]
            tag = "amended"
            message = f"Date provide is not a valid date. Set to default."
    else:
        # print(issues.keys())
        original, tag, message = mapSingleIssue(field, issues)
    return {"original": original, "tag": tag, "message": message}


def splitCoord(pt):
    # keys = list(issue.keys())
    # v = issue[keys[0]]
    coords = pt.split(",")
    return coords[0], coords[1]


def coordErrorObj(v, message):
    return {"original": v, "tag": "invalid", "message": message}


def formatIssuesForView(issues):
    for row in issues.keys():
        geox_issue = None
        for field in issues[row].keys():
            issues_with_field = issues[row][field]
            if field == "GeoX,GeoY":
                keys = list(issues_with_field.keys())
                x, y = splitCoord(issues_with_field[keys[0]])
                if "outside England" in keys[0]:
                    geox_issue = coordErrorObj(
                        x, "Coordinate provided is outside England"
                    )
                    geoy_issue = coordErrorObj(
                        y, "Coordinate provided is outside England"
                    )
                elif "out of range" in keys[0]:
                    geox_issue = coordErrorObj(
                        x, "Coordinate provided is not recognised"
                    )
                    geoy_issue = coordErrorObj(
                        y, "Coordinate provided is not recognised"
                    )
            else:
                issues[row][field] = generateIssueMessage(field, issues_with_field)
        if geox_issue is not None:
            issues[row]["GeoX"] = geox_issue
            issues[row]["GeoY"] = geoy_issue
    return issues


def urlForIssues(resource_hash):
    return f"https://digital-land-production-collection-dataset.s3.eu-west-2.amazonaws.com/brownfield-land-collection/issue/brownfield-land/{resource_hash}.csv"


def extractFromIssuesFile(resource_hash):
    # get the relevant issues for resource
    issues = pd.read_csv(urlForIssues(resource_hash), sep=",")
    issues_json = json.loads(issues.to_json(orient="records"))
    return formatIssuesForView(extractIssueData(issues_json))


def testIssueMapper():
    issues = pd.read_csv(csv_file_path, sep=",")
    issues_json = json.loads(issues.to_json(orient="records"))

    # map sample file by resource
    issue_resource = {}
    for row in issues_json:
        issue_resource.setdefault(row["resource"], {"issue": []})
        issue_resource[row["resource"]]["issue"].append(row)

    for resource_hash in issue_resource.keys():
        print(f"Extracting issues for resource: {resource_hash}")
        formatted_issues = formatIssuesForView(
            extractIssueData(issue_resource[resource_hash]["issue"])
        )
        print(formatted_issues)
        print(f"=========================")


# print(extractFromIssuesFile('f1e218c96f99e378fdbaed9a426c6b44d0e7d3b5fec63e201625047643c6da74'))