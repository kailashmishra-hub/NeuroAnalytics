import base64
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen
from dotenv import load_dotenv
from PIL import Image, ImageDraw

folder = Path(__file__).resolve().parent
load_dotenv(folder / '.env')
image = (folder / 'RawReports/MRI_01.png').read_bytes()

payload = {
    'model': 'jev-1.14.0',
    'state': {'document_image': 'mri-image-8f6d2a'},
    'assets': {
        'mri-image-8f6d2a': {
            'type': 'image',
            'format': 'png',
            'data_base64': base64.b64encode(image).decode('ascii'),
        }
    },

'questions': {
    'affected_region_B': {
        'type': 'choice',
        'instructions': (
            'Examine only the upper-row MRI panel labelled B in '
            '`document_image`. Which anatomical region contains the '
            'areas indicated by the white arrows? '
            'Select Unable to determine if localization is uncertain. '
            'Do not diagnose cerebral palsy or infer clinical severity.'
        ),
        'criteria': {
            'Periventricular white matter':
                'White matter surrounding the lateral ventricles.',
            'Cerebral cortex':
                'The outer cortical layer of the cerebral hemispheres.',
            'Basal ganglia or thalamus':
                'Deep gray-matter structures.',
            'Cerebellum':
                'The cerebellar region.',
            'Unable to determine':
                'The anatomical region cannot be identified reliably.'
        }
    },
    'marked_region_B': {
        'type': 'box',
        'instructions': (
            'In the upper-row panel labelled B in `document_image`, '
            'locate the tissue region immediately around the tip of '
            'the white arrow on the image-left side. '
            'Return a tight rectangle around that single region, '
            'excluding the other panels and the arrow shaft.'
        )
    },
'hie_related_pattern': {
    'type': 'choice',
    'instructions': (
        'For educational review, assess only upper-row panel B '
        'in `document_image`. Are the visible findings suggestive '
        'of chronic hypoxic-ischaemic injury? Consider alternative '
        'explanations and image limitations. Do not establish the '
        'cause or timing of injury from this image alone. '
        'Annotations are not proof of a diagnosis.'
    ),
    'criteria': {
        'Potentially suggestive': (
            'Visible findings may be compatible with chronic '
            'hypoxic-ischaemic injury, but require specialist confirmation.'
        ),
        'No clear supporting features': (
            'No clear supporting features are visible in this panel; '
            'this does not exclude previous injury.'
        ),
        'Indeterminate': (
            'The findings are nonspecific or the image and clinical '
            'information are insufficient.'
        )
    }
    },
     'hie_sequelae_location': {
      'type': 'box',
      'instructions': (
        'For educational review, examine upper-row panel B in '
        '`document_image`. Locate the single most clearly visible '
        'region that may represent chronic hypoxic-ischaemic injury '
        'sequelae. Return a tight rectangle around that region, '
        'excluding other panels, labels and annotation arrows. '
        'Do not assume the cause of an abnormality is HIE solely '
        'because it is highlighted.'
    )
},

'cerebral_palsy_status': {
    'type': 'choice',
    'instructions': (
        'What do the supplied clinical notes establish about '
        'cerebral palsy? Do not diagnose from the MRI alone.'
    ),
    'criteria': {
        'Confirmed diagnosis':
            'Clinical notes explicitly document a clinician-confirmed CP diagnosis.',
        'Suspected or under assessment':
            'Clinical notes explicitly describe suspected CP or ongoing assessment.',
        'Explicitly ruled out':
            'Clinical notes explicitly state that CP was ruled out.',
        'Insufficient information':
            'No clear clinical conclusion is supplied, records conflict, or only imaging is provided.'
    }
},

'adhd_status': {
    'type': 'choice',
    'instructions': (
        'What do the supplied clinical notes establish about ADHD? '
        'Do not infer ADHD from MRI appearance or a CP diagnosis.'
    ),
    'criteria': {
        'Confirmed diagnosis':
            'Clinical notes explicitly document a specialist-confirmed ADHD diagnosis.',
        'Suspected or under assessment':
            'Clinical notes explicitly describe suspected ADHD or ongoing assessment.',
        'Explicitly ruled out':
            'Clinical notes explicitly state that ADHD was ruled out.',
        'Insufficient information':
            'No clear clinical conclusion is supplied, records conflict, or only imaging is provided.'
    }
},

'autism_status': {
    'type': 'choice',
    'instructions': (
        'What do the supplied clinical notes establish about autism? '
        'Do not infer autism from MRI appearance or a CP diagnosis.'
    ),
    'criteria': {
        'Confirmed diagnosis':
            'Clinical notes explicitly document a clinician-confirmed autism diagnosis.',
        'Suspected or under assessment':
            'Clinical notes explicitly describe suspected autism or ongoing assessment.',
        'Explicitly ruled out':
            'Clinical notes explicitly state that autism was ruled out.',
        'Insufficient information':
            'No clear clinical conclusion is supplied, records conflict, or only imaging is provided.'
    }
}

}
}
request = Request(
    'https://api.typesafe.ai/v1/systemone',
    data=json.dumps(payload).encode('utf-8'),
    headers={
        'Authorization': f"Bearer {os.environ['TYPESAFE_API_KEY']}",
        'Content-Type': 'application/json',
        'TypeSafe-Danger-Zone-Images': 'true',
    },
    method='POST',
)


with urlopen(request, timeout=180) as response:
    result = json.load(response)

print(json.dumps(result, indent=2))

if result['answers']['affected_region_B']['choice'] == 'Unable to determine':
    print('Unable to determine the affected region.')
else:
    picture = Image.open(folder / 'RawReports/MRI_01.png').convert('RGB')
    width, height = picture.size
    box = result['answers']['marked_region_B']['box']
    box1=result['answers']['hie_sequelae_location']['box']

    ImageDraw.Draw(picture).rectangle(
        (
            box['left'] * width,
            box['top'] * height,
            box['right'] * width,
            box['bottom'] * height,
        ),
        outline='red',
        width=5,
    )

    ImageDraw.Draw(picture).rectangle(
        (
            box1['left'] * width,
            box1['top'] * height,
            box1['right'] * width,
            box1['bottom'] * height,
        ),
        outline='blue',
        width=5,
    )

    picture.save(folder / 'RawReports/Pattern_Recognition/highlighted.jpg')
    print('Open RawReports/Pattern_Recognition/highlighted.jpg to see the predicted affected area location.')
