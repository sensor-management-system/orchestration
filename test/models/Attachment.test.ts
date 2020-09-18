import { Attachment } from '@/models/Attachment'

describe('Attachment Models', () => {
  test('create a Attachment from an object', () => {
    const attachment = Attachment.createFromObject({ id: '1', url: 'https://foo/test.png', label: 'Testpicture' })
    expect(typeof attachment).toBe('object')
    expect(attachment).toHaveProperty('id', '1')
    expect(attachment).toHaveProperty('url', 'https://foo/test.png')
    expect(attachment).toHaveProperty('label', 'Testpicture')
  })
})
